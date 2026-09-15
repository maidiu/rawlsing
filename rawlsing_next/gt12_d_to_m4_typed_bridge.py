"""Bounded GT12 closure bridge: PRE-V3 relation admission -> M1/V554 -> M4/V558.

This module is intentionally narrow.  It consumes the actual typed
Prev3FieldForgeRelationAdmission emitted by the GT12-D jurisdiction and
re-expresses its exact PRE553 ExactRef/AuthorityRef material for the
relation-specific GT12-E ingress without reducing hashes/versions to labels.

It then offers a bounded helper that uses the existing M4 V557/V558
implementation.  It creates no relation admission, empirical M1 basis, V553,
V555/V556 object, actor fact, or positive V3 transition authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef as Pre553AuthorityRef,
    ExactRef as Pre553ExactRef,
)
from rawlsing_next.wave1_ff_prev3_relation_admission import (
    AdmissionDecision,
    GT2_DOWNSTREAM_CONTRACT,
    GT2_RELATION_FAMILY,
    GT2_TARGET_USE,
    Prev3FieldForgeRelationAdmission,
    RECEIPT_CONTRACT_ID,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1DecisionState,
    M1Evaluation,
    semantic_hash,
)
from rawlsing_next.m1_admitted_field_forge_relation_v554_ingress import (
    RELATION_ADMISSION_REF_KIND,
    RELATION_ADMISSION_SCHEMA,
    RELATION_BASIS_KIND,
    RELATION_INFORMATION_LOSS,
    RELATION_M1_CONTRACT_ID,
    RELATION_TEMPORAL_DISPOSITION,
    SIG_004,
    RelationBasisPreparation,
    RelationPreparationState,
    evaluate_m1_admitted_field_forge_relation_v554,
    prepare_admitted_field_forge_relation_basis,
)
from rawlsing_next.m4_m1_evaluation_binding import (
    _issue_validated_relation_producer_use_binding,
    structural_objects_from_accepted_m1,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef as M4AuthorityRef,
    ContextQueryItem,
    M4IntegrityError,
    RepositoryEntry,
    ResolutionResult,
    V557DecisionState,
    V557PublicationBundle,
    V557PublicationEntry,
    V558RepositoryBundle,
    build_v557_publication_bundle,
    build_v558_repository_bundle,
    exact_resolution_key,
    govern_v557,
    make_context_query,
    make_producer_locator,
    resolve_v558,
)
from rawlsing_next.gt12_permission_translation_authority import (
    ADOPTED_ADOPTION_RECEIPT_REF,
    ADOPTED_AUTHORITY_REF,
    ADOPTED_PRODUCER_ALLOWED_USES,
    ADOPTED_V557_ALLOWED_USES,
    ADOPTED_V558_REQUESTED_USES,
    GT12PermissionTranslationError,
    derive_adopted_permission_binding,
    require_exact_downstream_use_shape,
)


BRIDGE_CONTRACT_ID = "GT12_D_TO_E_TO_M4_V558_TYPED_BRIDGE@1.0.0"
FOCAL_STRUCTURAL_PROPOSITION = (
    "GT2_Q86B_CONDITIONAL_SUPPORT_Q86A_COUNT_PROFILE_WITHIN_SCOPE"
)
EXPECTED_RELATION_OWNER_JURISDICTION = "FIELD_FORGE_ACTOR_INDEPENDENT_RELATION_OWNER"


class GT12TypedBridgeError(ValueError):
    """Exact typed D->E->M4/V558 bridge invariant failed."""


def _ref(ref: Pre553ExactRef, name: str) -> dict[str, str]:
    if not isinstance(ref, Pre553ExactRef):
        raise GT12TypedBridgeError(f"{name} must be PRE553 ExactRef")
    return ref.as_dict()


def _auth(ref: Pre553AuthorityRef, name: str) -> dict[str, str]:
    if not isinstance(ref, Pre553AuthorityRef):
        raise GT12TypedBridgeError(f"{name} must be PRE553 AuthorityRef")
    return ref.as_dict()


def _rule(value: Mapping[str, Any]) -> dict[str, str]:
    if not isinstance(value, Mapping) or set(value) != {"id", "version", "hash"}:
        raise GT12TypedBridgeError(
            "V554 rule must preserve exact id/version/hash fields"
        )
    out = {}
    for key in ("id", "version", "hash"):
        item = value[key]
        if not isinstance(item, str) or not item.strip():
            raise GT12TypedBridgeError(f"V554 rule {key} must be non-empty")
        out[key] = item.strip()
    if len(out["hash"]) != 64 or any(ch not in "0123456789abcdef" for ch in out["hash"]):
        raise GT12TypedBridgeError("V554 rule hash must be lowercase sha256")
    return out


def _authority_token(ref: Pre553AuthorityRef) -> str:
    return (
        f"{ref.authority_id}@{ref.authority_version}"
        f"#sha256:{ref.authority_content_hash}"
    )


def _participant_material(admission: Prev3FieldForgeRelationAdmission) -> list[dict[str, Any]]:
    participants = [participant.material() for participant in admission.participants]
    if [item["role"] for item in participants] != ["CONDITIONER", "TARGET"]:
        raise GT12TypedBridgeError(
            "positive GT2 admission must preserve CONDITIONER then TARGET roles"
        )
    if [item["ordinal"] for item in participants] != [0, 1]:
        raise GT12TypedBridgeError("positive GT2 admission participant ordinals drifted")
    if [item["native_variable"] for item in participants] != ["Q86B", "Q86A"]:
        raise GT12TypedBridgeError(
            "positive GT2 admission must preserve Q86B conditioner and Q86A target"
        )
    return participants


def _require_positive_admission(
    admission: Prev3FieldForgeRelationAdmission,
) -> None:
    if not isinstance(admission, Prev3FieldForgeRelationAdmission):
        raise GT12TypedBridgeError(
            "bridge requires actual Prev3FieldForgeRelationAdmission"
        )
    if admission.decision is not AdmissionDecision.ADMITTED or not admission.is_positive:
        raise GT12TypedBridgeError("bridge accepts only positive ADMITTED D receipt")
    if admission.target_use != GT2_TARGET_USE:
        raise GT12TypedBridgeError("D receipt target use is not STRUCTURAL_MEDIATION_INPUT")
    if admission.downstream_contract != RELATION_M1_CONTRACT_ID:
        raise GT12TypedBridgeError("D receipt downstream contract is not exact relation M1")
    if admission.relation_information_loss_declaration != RELATION_INFORMATION_LOSS:
        raise GT12TypedBridgeError("D relation information-loss declaration drifted")
    if admission.admission_information_loss_declaration != RELATION_INFORMATION_LOSS:
        raise GT12TypedBridgeError("D admission information-loss declaration drifted")
    if admission.relation_content_hash_echo != admission.relation_ref.content_hash:
        raise GT12TypedBridgeError("D relation content-hash echo mismatch")
    if admission.relation_rule_content_hash_echo != admission.relation_rule_ref.content_hash:
        raise GT12TypedBridgeError("D relation-rule content-hash echo mismatch")
    if GT2_TARGET_USE not in admission.target_use_permissions:
        raise GT12TypedBridgeError("D positive receipt lacks exact target-use permission")
    if not set(admission.target_use_permissions).issubset(
        set(admission.relation_permission_ceiling)
    ):
        raise GT12TypedBridgeError("D receipt permission widens relation ceiling")
    if admission.applicable_negative_denial_noncomparability_refs:
        raise GT12TypedBridgeError(
            "positive D receipt may not launder applicable typed negative refs"
        )
    if not admission.relation_semantic_identity_refs:
        raise GT12TypedBridgeError("D receipt lost relation semantic identity")
    if not admission.native_scope_identity_refs or not admission.source_universe_refs:
        raise GT12TypedBridgeError("D receipt lost exact scope/universe identity")
    if not admission.relation_authority_refs:
        raise GT12TypedBridgeError("D receipt lost exact relation authority")
    if not admission.dependency_refs:
        raise GT12TypedBridgeError("D receipt lost dependency/provenance closure")
    _participant_material(admission)


def _closure_identities(
    admission: Prev3FieldForgeRelationAdmission,
) -> list[Any]:
    """Lossless mixed PRE553 ref/authority closure for E projection."""
    return [
        _ref(admission.admission_current_selection_ref, "admission_current_selection_ref"),
        _ref(admission.admission_rule_ref, "admission_rule_ref"),
        _auth(admission.admission_authority_ref, "admission_authority_ref"),
        _ref(admission.relation_ref, "relation_ref"),
        _ref(admission.relation_rule_ref, "relation_rule_ref"),
        _ref(
            admission.producer_replay_locator_or_reference_root,
            "producer_replay_locator_or_reference_root",
        ),
        *[_auth(x, "relation_authority_ref") for x in admission.relation_authority_refs],
        *[_ref(x, "dependency_ref") for x in admission.dependency_refs],
        *[_ref(x, "relation_semantic_identity_ref") for x in admission.relation_semantic_identity_refs],
        *[_ref(x, "native_scope_identity_ref") for x in admission.native_scope_identity_refs],
        *[_ref(x, "source_universe_ref") for x in admission.source_universe_refs],
        _ref(admission.risk_set_ref, "risk_set_ref"),
    ]


def _admission_mapping(
    admission: Prev3FieldForgeRelationAdmission,
) -> dict[str, Any]:
    receipt_ref = admission.ref
    participants = _participant_material(admission)
    closure = _closure_identities(admission)
    return {
        "schema_id": RELATION_ADMISSION_SCHEMA,
        "field_forge_relation_admission_id": receipt_ref.object_id,
        "field_forge_relation_admission_content_hash": receipt_ref.content_hash,
        "field_forge_relation_ref": _ref(admission.relation_ref, "relation_ref"),
        "relation_owner_ref_or_id": admission.relation_owner,
        "relation_rule_ref": _ref(admission.relation_rule_ref, "relation_rule_ref"),
        "relation_typed_state": admission.relation_typed_state,
        "admission_authority_ref": _auth(
            admission.admission_authority_ref, "admission_authority_ref"
        ),
        "admission_rule_ref": _ref(admission.admission_rule_ref, "admission_rule_ref"),
        "admission_decision_state": admission.decision.value,
        "target_use_ref": admission.target_use,
        "requested_downstream_owner_or_contract_family": admission.downstream_contract,
        "relation_semantic_identity_refs": [
            _ref(x, "relation_semantic_identity_ref")
            for x in admission.relation_semantic_identity_refs
        ],
        "native_scope_identity_refs": [
            _ref(x, "native_scope_identity_ref")
            for x in admission.native_scope_identity_refs
        ],
        "source_universe_refs": [
            _ref(x, "source_universe_ref") for x in admission.source_universe_refs
        ],
        "risk_set_refs": [_ref(admission.risk_set_ref, "risk_set_ref")],
        "relation_participant_role_order_cardinality_refs": participants,
        "target_use_permission_refs": list(admission.target_use_permissions),
        "effective_time_or_interval_refs_required_by_target_use": [],
        "estimand_refs": [],
        "measure_and_weight_authority_refs": [],
        "source_relation_comparability_authority_refs_where_required": [],
        "applicable_negative_denial_noncomparability_refs": [
            _ref(x, "negative_or_limit_ref")
            for x in admission.applicable_negative_denial_noncomparability_refs
        ],
        "interpretation_critical_authority_refs": [],
        "relation_information_loss_declaration": (
            admission.relation_information_loss_declaration
        ),
        "producer_replay_locator_or_reference_root": _ref(
            admission.producer_replay_locator_or_reference_root,
            "producer_replay_locator_or_reference_root",
        ),
        "authority_current_selection_dependency_provenance_refs": closure,
    }


@dataclass(frozen=True)
class TypedDToEBridge:
    admission_ref: Pre553ExactRef
    payload: Mapping[str, Any]
    preparation: RelationBasisPreparation

    def __post_init__(self) -> None:
        if not isinstance(self.admission_ref, Pre553ExactRef):
            raise GT12TypedBridgeError("bridge admission_ref must remain PRE553 ExactRef")
        if not isinstance(self.preparation, RelationBasisPreparation):
            raise GT12TypedBridgeError("bridge preparation type mismatch")


def prepare_typed_d_to_e_relation_basis(
    admission: Prev3FieldForgeRelationAdmission,
    *,
    v554_rule_ref: Mapping[str, Any],
    focal_structural_proposition_ref: str = FOCAL_STRUCTURAL_PROPOSITION,
) -> TypedDToEBridge:
    """Losslessly translate one actual positive D receipt into E preparation."""
    _require_positive_admission(admission)
    rule = _rule(v554_rule_ref)
    if (
        not isinstance(focal_structural_proposition_ref, str)
        or not focal_structural_proposition_ref.strip()
    ):
        raise GT12TypedBridgeError("focal structural proposition must be exact non-empty id")
    focal = focal_structural_proposition_ref.strip()

    admitted = _admission_mapping(admission)
    receipt_ref = admission.ref
    participants = admitted["relation_participant_role_order_cardinality_refs"]
    projection = {
        "relation_admission_ref": _ref(receipt_ref, "admission.ref"),
        "relation_admission_authority_ref": admitted["admission_authority_ref"],
        "relation_admission_rule_ref": admitted["admission_rule_ref"],
        "relation_admission_decision_state": admission.decision.value,
        "field_forge_relation_ref": admitted["field_forge_relation_ref"],
        "relation_semantic_identity_refs": admitted["relation_semantic_identity_refs"],
        "relation_participant_role_order_cardinality_refs": participants,
        "focal_structural_proposition_ref": focal,
        "native_scope_identity_refs": admitted["native_scope_identity_refs"],
        "source_universe_refs": admitted["source_universe_refs"],
        "risk_set_refs": admitted["risk_set_refs"],
        "target_use_ref": admission.target_use,
        "requested_downstream_owner_or_contract_family": admission.downstream_contract,
        "target_use_permission_refs": admitted["target_use_permission_refs"],
        "effective_time_or_interval_refs_required_by_target_use": [],
        "estimand_refs": [],
        "measure_and_weight_authority_refs": [],
        "source_relation_comparability_authority_refs_where_required": [],
        "applicable_negative_denial_noncomparability_refs": (
            admitted["applicable_negative_denial_noncomparability_refs"]
        ),
        "interpretation_critical_authority_refs": (
            admitted["interpretation_critical_authority_refs"]
        ),
        "producer_replay_locator_or_reference_root": (
            admitted["producer_replay_locator_or_reference_root"]
        ),
        "authority_current_selection_dependency_provenance_refs": (
            admitted["authority_current_selection_dependency_provenance_refs"]
        ),
        "information_loss_declaration": RELATION_INFORMATION_LOSS,
        "temporal_semantic_disposition": RELATION_TEMPORAL_DISPOSITION,
    }

    equivalence_key = {
        "focal_structural_proposition_ref": focal,
        "target_use": GT2_TARGET_USE,
        "v554_rule_id": rule["id"],
        "v554_rule_version": rule["version"],
        "v554_rule_hash": rule["hash"],
        "basis_semantic_class": RELATION_BASIS_KIND,
        "rule_relevant_structural_semantic_identity_fingerprint": semantic_hash(
            list(projection["relation_semantic_identity_refs"])
        ),
        "relation_participant_role_order_cardinality_fingerprint": semantic_hash(
            list(projection["relation_participant_role_order_cardinality_refs"])
        ),
        "native_scope_identity_fingerprint": semantic_hash(
            list(projection["native_scope_identity_refs"])
        ),
        "rule_relevant_effective_time_semantics_fingerprint": semantic_hash(
            {
                "disposition": RELATION_TEMPORAL_DISPOSITION,
                "refs": [],
            }
        ),
        "originating_admitted_relation_lineage_fingerprint": semantic_hash(
            projection["relation_admission_ref"]
        ),
        "source_universe_fingerprint": semantic_hash(
            list(projection["source_universe_refs"])
        ),
        "estimand_fingerprint": semantic_hash([]),
        "measure_and_weight_authority_fingerprint": semantic_hash([]),
        "rule_relevant_source_relation_comparability_authority_fingerprint": (
            semantic_hash([])
        ),
        "interpretation_critical_semantic_authority_fingerprint": semantic_hash(
            list(projection["interpretation_critical_authority_refs"])
        ),
    }

    selected_semantics = {
        "relation_family": GT2_RELATION_FAMILY,
        "field_forge_relation_ref": admitted["field_forge_relation_ref"],
        "field_forge_relation_owner": admission.relation_owner,
        "relation_rule_ref": admitted["relation_rule_ref"],
        "participant_bindings": participants,
        "count_profile_only": True,
        "ratio_present": False,
        "temporal_semantics_added": False,
    }
    payload = {
        "relation_admission": admitted,
        "basis_ref": {
            "kind": RELATION_BASIS_KIND,
            "object_id": receipt_ref.object_id,
            "content_hash": receipt_ref.content_hash,
        },
        "projection": projection,
        "projection_hash": semantic_hash(projection),
        "equivalence_key": equivalence_key,
        "selected_rule_relevant_basis_semantics": selected_semantics,
        "focal_structural_proposition_ref": focal,
    }
    preparation = prepare_admitted_field_forge_relation_basis(payload)
    if preparation.state is not RelationPreparationState.RELATION_BASIS_READY:
        raise GT12TypedBridgeError(
            f"typed D->E preparation failed closed: {preparation.state.value}: "
            f"{preparation.reason}"
        )
    return TypedDToEBridge(receipt_ref, payload, preparation)


def evaluate_typed_d_to_e_at_v554(
    admission: Prev3FieldForgeRelationAdmission,
    *,
    governed_use_id: str,
    v554_rule_ref: Mapping[str, Any],
    publication_authority: Mapping[str, Any],
    focal_structural_proposition_ref: str = FOCAL_STRUCTURAL_PROPOSITION,
) -> tuple[TypedDToEBridge, M1Evaluation]:
    """Prepare and execute only the relation-specific SIG-004 M1/V554 ingress."""
    bridge = prepare_typed_d_to_e_relation_basis(
        admission,
        v554_rule_ref=v554_rule_ref,
        focal_structural_proposition_ref=focal_structural_proposition_ref,
    )
    authority_bundle = {
        "bridge_contract": BRIDGE_CONTRACT_ID,
        "admission_ref": _ref(admission.ref, "admission.ref"),
        "admission_authority_ref": _auth(
            admission.admission_authority_ref, "admission_authority_ref"
        ),
        "admission_rule_ref": _ref(admission.admission_rule_ref, "admission_rule_ref"),
        "admission_current_selection_ref": _ref(
            admission.admission_current_selection_ref,
            "admission_current_selection_ref",
        ),
        "field_forge_relation_ref": _ref(admission.relation_ref, "relation_ref"),
        "field_forge_relation_owner": admission.relation_owner,
        "relation_rule_ref": _ref(admission.relation_rule_ref, "relation_rule_ref"),
        "relation_authority_refs": [
            _auth(x, "relation_authority_ref") for x in admission.relation_authority_refs
        ],
        "dependency_refs": [_ref(x, "dependency_ref") for x in admission.dependency_refs],
        "producer_replay_ref": _ref(
            admission.producer_replay_locator_or_reference_root,
            "producer_replay_locator_or_reference_root",
        ),
        "historical_authority_material_hash": admission.historical_authority_material_hash,
    }
    required_snapshots = tuple(
        sorted(
            {
                _authority_token(admission.admission_authority_ref),
                *(_authority_token(x) for x in admission.relation_authority_refs),
            }
        )
    )
    evaluation = evaluate_m1_admitted_field_forge_relation_v554(
        governed_use_id=governed_use_id,
        v554_rule_ref=_rule(v554_rule_ref),
        focal_structural_proposition_ref=focal_structural_proposition_ref,
        preparations=(bridge.preparation,),
        required_authority_snapshot_refs=required_snapshots,
        authority_bundle_material=authority_bundle,
        producer_reference_spine_fingerprint=semantic_hash(authority_bundle),
        conditions=(),
        publication_authority=publication_authority,
    )
    if (
        evaluation.contract_id != RELATION_M1_CONTRACT_ID
        or evaluation.required_basis_kind != RELATION_BASIS_KIND
    ):
        raise GT12TypedBridgeError(
            "relation-specific M1 contract/basis identity was not preserved"
        )
    if evaluation.decision_state is M1DecisionState.ELIGIBLE:
        if (
            evaluation.f1 is None
            or evaluation.f1.get("material", {}).get("signature_id") != SIG_004
        ):
            raise GT12TypedBridgeError("eligible relation M1 lost exact SIG-004")
    return bridge, evaluation


@dataclass(frozen=True)
class RelationV558Terminal:
    evaluation: M1Evaluation
    publication: V557PublicationBundle
    repository: V558RepositoryBundle
    resolution: ResolutionResult
    resolution_keys: tuple[str, ...]
    permission_binding: Mapping[str, Any]


def _require_evaluation_matches_admission(
    admission: Prev3FieldForgeRelationAdmission,
    evaluation: M1Evaluation,
) -> None:
    if evaluation.f1 is None:
        raise GT12TypedBridgeError("eligible relation M1 lacks F1 lineage")
    expected_admission_ref = admission.ref.as_dict()
    expected_relation_ref = admission.relation_ref.as_dict()
    admission_refs = tuple(evaluation.f1.get("originating_relation_admission_exact_refs", ()))
    relation_refs = tuple(evaluation.f1.get("originating_field_forge_relation_exact_refs", ()))
    if admission_refs != (expected_admission_ref,):
        raise GT12TypedBridgeError("M1 relation admission exact ref/hash does not match permission authority input")
    if relation_refs != (expected_relation_ref,):
        raise GT12TypedBridgeError("M1 FIELD FORGE relation exact ref/hash does not match permission authority input")
    handoff = evaluation.direct_v557_handoff
    if not isinstance(handoff, Mapping) or handoff.get("route") != "V554_TO_V557_DIRECT":
        raise GT12TypedBridgeError("relation M1 direct V554_TO_V557 handoff missing")


def publish_and_resolve_relation_v554_at_current_m4(
    admission: Prev3FieldForgeRelationAdmission,
    evaluation: M1Evaluation,
    *,
    v557_allowed_uses: Sequence[str],
    requested_resolution_uses: Sequence[str],
    v557_authority_ref: M4AuthorityRef,
    v557_decision_state: V557DecisionState | str,
    permission_translation_authority_ref: M4AuthorityRef = ADOPTED_AUTHORITY_REF,
    permission_translation_adoption_ref: M4AuthorityRef = ADOPTED_ADOPTION_RECEIPT_REF,
    producer_rule_bindings: Sequence[M4AuthorityRef] = (),
) -> RelationV558Terminal:
    """Traverse M4 only under the adopted exact GT12 permission descent.

    The relation-specific producer ceiling is derived, never caller-selected.
    """
    if not isinstance(evaluation, M1Evaluation):
        raise GT12TypedBridgeError("M4 bridge requires exact M1Evaluation")
    if evaluation.contract_id != RELATION_M1_CONTRACT_ID:
        raise GT12TypedBridgeError(
            "empirical-direct or unknown M1 contract may not impersonate relation ingress"
        )
    if evaluation.required_basis_kind != RELATION_BASIS_KIND:
        raise GT12TypedBridgeError("M1 evaluation is not ADMITTED_FIELD_FORGE_RELATION")
    if evaluation.decision_state is not M1DecisionState.ELIGIBLE:
        raise GT12TypedBridgeError("only positive eligible relation M1 may reach V557")
    if not isinstance(v557_authority_ref, M4AuthorityRef):
        raise GT12TypedBridgeError("V557 authority must be exact current M4 AuthorityRef")
    if any(not isinstance(x, M4AuthorityRef) for x in producer_rule_bindings):
        raise GT12TypedBridgeError("producer rule bindings must be exact M4 AuthorityRef")

    try:
        permission_binding = derive_adopted_permission_binding(
            admission,
            authority_ref=permission_translation_authority_ref,
            adoption_receipt_ref=permission_translation_adoption_ref,
        )
        require_exact_downstream_use_shape(
            v557_decision_state=v557_decision_state,
            v557_allowed_uses=v557_allowed_uses,
            requested_resolution_uses=requested_resolution_uses,
        )
    except GT12PermissionTranslationError as exc:
        raise GT12TypedBridgeError(str(exc)) from exc
    _require_evaluation_matches_admission(admission, evaluation)
    try:
        validated_producer_use_binding = _issue_validated_relation_producer_use_binding(
            evaluation,
            permission_binding,
        )
    except M4IntegrityError as exc:
        raise GT12TypedBridgeError(str(exc)) from exc

    objects = structural_objects_from_accepted_m1(
        evaluation,
        validated_producer_use_binding=validated_producer_use_binding,
    )
    if not objects:
        raise GT12TypedBridgeError("eligible relation M1 produced no V554 objects")
    if {obj.producer_family for obj in objects} != {"V554"}:
        raise GT12TypedBridgeError("relation M1 may publish only V554 producer family")
    if any(obj.source_stage != "M1_RELATION_V554_TO_V557" for obj in objects):
        raise GT12TypedBridgeError("relation M1 attempted non-relation M4 source stage")
    if any(obj.producer_allowed_uses != ADOPTED_PRODUCER_ALLOWED_USES for obj in objects):
        raise GT12TypedBridgeError("relation V554 producer permission did not derive exact CONTEXT singleton")

    build_material = {
        "bridge_contract": BRIDGE_CONTRACT_ID,
        "m1_contract": evaluation.contract_id,
        "decision_state": evaluation.decision_state.value,
        "canonical_basis_semantic_id": evaluation.canonical_basis_semantic_id,
        "direct_v557_handoff": evaluation.direct_v557_handoff,
        "permission_translation_binding": dict(permission_binding),
    }
    build_hash = semantic_hash(build_material)
    build_id = f"GT12-D-E-M4-V558:{build_hash}"
    contract_hash = semantic_hash(
        {
            "contract_id": evaluation.contract_id,
            "basis_kind": evaluation.required_basis_kind,
            "signature": SIG_004,
            "permission_translation_binding_hash": permission_binding["binding_hash"],
        }
    )
    exact_rule_bindings = tuple(
        sorted(
            {
                *tuple(producer_rule_bindings),
                permission_translation_authority_ref,
                permission_translation_adoption_ref,
            },
            key=lambda ref: (ref.authority_id, ref.authority_version, ref.authority_hash),
        )
    )

    entries = []
    publication_entries = []
    for obj in objects:
        governance = govern_v557(
            obj,
            decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
            v557_allowed_uses=ADOPTED_V557_ALLOWED_USES,
            authority_ref=v557_authority_ref,
        )
        locator = make_producer_locator(
            obj,
            governance,
            logical_collection_kind="GT2_V554_ADMITTED_FIELD_FORGE_RELATION",
            authoritative_build_id=build_id,
            authoritative_build_hash=build_hash,
            producer_contract_id=evaluation.contract_id,
            producer_contract_version="1.0.0",
            producer_contract_hash=contract_hash,
            producer_rule_bindings=exact_rule_bindings,
            provenance_locator=(
                f"audit://GT12_D_TO_E_TO_V558/{permission_binding['binding_hash']}/{obj.content_hash}"
            ),
        )
        entry = RepositoryEntry(obj, governance, locator)
        entries.append(entry)
        publication_entries.append(V557PublicationEntry(obj, governance))

    publication = build_v557_publication_bundle(tuple(publication_entries))
    repository = build_v558_repository_bundle(publication, tuple(entries))
    keys = tuple(exact_resolution_key(entry.locator) for entry in entries)
    query = make_context_query(
        tuple(
            ContextQueryItem(key, ADOPTED_V558_REQUESTED_USES)
            for key in keys
        )
    )
    resolution = resolve_v558(repository, query)
    if resolution.receipt.result_state != "RESOLUTION_COMPLETE":
        raise GT12TypedBridgeError(
            "positive relation V558 exact resolution did not complete: "
            f"{resolution.receipt.result_state}"
        )
    if len(resolution.resolved_entries) != len(entries):
        raise GT12TypedBridgeError("V558 did not resolve every exact V554 publication root")
    if {item.canonical_producer_family for item in resolution.resolved_entries} != {"V554"}:
        raise GT12TypedBridgeError("V558 producer family drifted from V554")
    return RelationV558Terminal(
        evaluation,
        publication,
        repository,
        resolution,
        keys,
        permission_binding,
    )


__all__ = [
    "BRIDGE_CONTRACT_ID",
    "FOCAL_STRUCTURAL_PROPOSITION",
    "EXPECTED_RELATION_OWNER_JURISDICTION",
    "GT12TypedBridgeError",
    "TypedDToEBridge",
    "RelationV558Terminal",
    "prepare_typed_d_to_e_relation_basis",
    "evaluate_typed_d_to_e_at_v554",
    "publish_and_resolve_relation_v554_at_current_m4",
]
