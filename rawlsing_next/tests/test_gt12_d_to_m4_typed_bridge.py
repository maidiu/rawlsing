from __future__ import annotations

from copy import deepcopy
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.wave1_ff_prev3_relation_admission import (
    AdmissionDecision,
    ParticipantBinding,
    Prev3FieldForgeRelationAdmission,
)
from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID,
    SIGS as EMPIRICAL_M1_SIGS,
    semantic_hash,
)
from rawlsing_next.m1_admitted_field_forge_relation_v554_ingress import (
    RELATION_BASIS_KIND,
    RELATION_M1_CONTRACT_ID,
    SIG_004,
    RelationPreparationState,
    prepare_admitted_field_forge_relation_basis,
)
from rawlsing_next.m4_m1_evaluation_binding import (
    structural_objects_from_accepted_m1,
)
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef as M4AuthorityRef,
    ClosureIntegrityError,
    ContextQueryItem,
    M4IntegrityError,
    PermissionWideningError,
    V557DecisionState,
    make_context_query,
    resolve_v558,
)
from rawlsing_next.gt12_d_to_m4_typed_bridge import (
    EXPECTED_RELATION_OWNER_JURISDICTION,
    FOCAL_STRUCTURAL_PROPOSITION,
    GT12TypedBridgeError,
    evaluate_typed_d_to_e_at_v554,
    prepare_typed_d_to_e_relation_basis,
    publish_and_resolve_relation_v554_at_current_m4,
)


def _h(label: str) -> str:
    return semantic_hash({"gt12-closure-c": label})


def _ref(kind: str, label: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:gt12-closure-c:{label}", _h(f"ref:{kind}:{label}"))


def _auth(label: str, version: str = "R1") -> AuthorityRef:
    return AuthorityRef(
        f"AUTH-{label}",
        version,
        _h(f"authority:{label}:{version}"),
    )


def _m4_auth(label: str, version: str = "1.0.0") -> M4AuthorityRef:
    return M4AuthorityRef(
        f"M4-AUTH-{label}",
        version,
        _h(f"m4-authority:{label}:{version}"),
    )


def _v554_rule() -> dict[str, str]:
    return {
        "id": "V554-RULE-GT2-CONDITIONAL-SUPPORT",
        "version": "1.0.0",
        "hash": _h("v554-rule"),
    }


def _publication_authority(use: str) -> dict[str, object]:
    return {
        "authority_id": "V557-PUBLISH-GT2-RELATION",
        "authority_version": "1.0.0",
        "authority_hash": _h("m1-publication-authority"),
        "producer": "V554",
        "publisher": "V557",
        "governed_use_id": use,
        "rule_ref": _v554_rule(),
        "decision": "AUTHORIZED",
        "allowed_object_families": ["F1", "F2", "B1"],
    }


def _admission() -> Prev3FieldForgeRelationAdmission:
    relation = _ref(
        "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0",
        "field-forge-relation",
    )
    relation_rule = _ref(
        "FIELD_FORGE_RELATION_RULE",
        "exact-conditional-support-profile-within-scope",
    )
    admission_rule = _ref(
        "FIELD_FORGE_RELATION_ADMISSION_RULE",
        "FIELD_FORGE_RELATION_ADMISSION_RULE@1.0.0",
    )
    admission_authority = _auth("PREV3-RELATION-ADMISSION", "R1")
    selection = _ref(
        "RELATION_ADMISSION_CURRENT_SELECTION",
        "gt2-current-selection",
    )
    conditioner = ParticipantBinding(
        "CONDITIONER",
        0,
        "Q86B",
        "question_impl.phase0.2fb3a62609dad4c1306d",
        "cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4",
        _ref("QUESTION_IMPLEMENTATION", "Q86B"),
    )
    target = ParticipantBinding(
        "TARGET",
        1,
        "Q86A",
        "question_impl.phase0.67f036c0efb7fb98ff4a",
        "cssu.r1.afrobarometer.r5.d8478014cb0a506fe6c4",
        _ref("QUESTION_IMPLEMENTATION", "Q86A"),
    )
    semantic_identity = _ref(
        "FIELD_FORGE_RELATION_SEMANTIC_IDENTITY",
        "q86b-conditions-q86a-count-profile",
    )
    scope = _ref("NATIVE_SCOPE", "afrobarometer-r5-q86-riskset")
    universe = _ref("EmpiricalUniverse@1.0.0", "afrobarometer-r5")
    risk = ExactRef(
        "RISK_SET",
        "FIRST_GENUINE_CANARY_COMMON_COEXPOSURE_RISK_SET@1",
        "0484fa5c0440c34e9b1f28b385f3ef6c3302eaeb11c3c5b663441553ea11313b",
    )
    relation_authority = _auth("FIELD-FORGE-RELATION", "R2")
    replay = _ref("FIELD_FORGE_RELATION_REPLAY", "gt2-replay")
    joint_fact = _ref("EmpiricalFact@1.0.0", "gt2-joint-fact")
    joint_query = _ref("EmpiricalQuerySpec@1.0.0", "gt2-joint-query")
    source = ExactRef(
        "SOURCE_ARTIFACT",
        "Data/Afro Barometer Round 5.sav",
        "c9200ba325bbff6132a7813883eb344202abb16be4f79475cb455243d3c7b651",
    )
    return Prev3FieldForgeRelationAdmission(
        decision=AdmissionDecision.ADMITTED,
        reason_code="EXACT_GT2_RELATION_ADMITTED_FOR_STRUCTURAL_MEDIATION_INPUT",
        relation_ref=relation,
        relation_content_hash_echo=relation.content_hash,
        relation_owner=EXPECTED_RELATION_OWNER_JURISDICTION,
        relation_rule_ref=relation_rule,
        relation_rule_content_hash_echo=relation_rule.content_hash,
        relation_typed_state="SUPPORTED",
        admission_rule_ref=admission_rule,
        admission_authority_ref=admission_authority,
        admission_current_selection_ref=selection,
        target_use="STRUCTURAL_MEDIATION_INPUT",
        downstream_contract=RELATION_M1_CONTRACT_ID,
        target_use_permissions=("STRUCTURAL_MEDIATION_INPUT",),
        relation_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
        relation_semantic_identity_refs=(semantic_identity,),
        native_scope_identity_refs=(scope,),
        source_universe_refs=(universe,),
        risk_set_ref=risk,
        participants=(conditioner, target),
        applicable_negative_denial_noncomparability_refs=(),
        relation_authority_refs=(relation_authority,),
        dependency_refs=(
            relation,
            relation_rule,
            replay,
            joint_fact,
            joint_query,
            source,
            universe,
            risk,
        ),
        relation_information_loss_declaration="NONE__REFERENCE_PRESERVING",
        admission_information_loss_declaration="NONE__REFERENCE_PRESERVING",
        producer_replay_locator_or_reference_root=replay,
        historical_authority_material_hash=_h("historical-authority-material"),
    )


def _evaluate():
    admission = _admission()
    use = "GT2_STRUCTURAL_MEDIATION_REVIEW"
    bridge, evaluation = evaluate_typed_d_to_e_at_v554(
        admission,
        governed_use_id=use,
        v554_rule_ref=_v554_rule(),
        publication_authority=_publication_authority(use),
    )
    return admission, bridge, evaluation


def test_actual_pre553_ref_authority_material_survives_d_to_e_losslessly():
    admission = _admission()
    bridge = prepare_typed_d_to_e_relation_basis(
        admission,
        v554_rule_ref=_v554_rule(),
    )
    assert bridge.preparation.state is RelationPreparationState.RELATION_BASIS_READY
    payload = bridge.payload
    admitted = payload["relation_admission"]
    projection = payload["projection"]

    assert admitted["field_forge_relation_ref"] == admission.relation_ref.as_dict()
    assert admitted["relation_rule_ref"] == admission.relation_rule_ref.as_dict()
    assert admitted["admission_rule_ref"] == admission.admission_rule_ref.as_dict()
    assert admitted["admission_authority_ref"] == admission.admission_authority_ref.as_dict()
    assert admitted["relation_owner_ref_or_id"] == EXPECTED_RELATION_OWNER_JURISDICTION
    assert projection["relation_admission_ref"] == admission.ref.as_dict()
    assert projection["risk_set_refs"] == [admission.risk_set_ref.as_dict()]
    assert projection["producer_replay_locator_or_reference_root"] == (
        admission.producer_replay_locator_or_reference_root.as_dict()
    )
    assert admission.admission_authority_ref.as_dict() in (
        projection["authority_current_selection_dependency_provenance_refs"]
    )
    assert admission.relation_ref.as_dict() in (
        projection["authority_current_selection_dependency_provenance_refs"]
    )


def test_positive_typed_d_to_e_evaluates_only_relation_sig004_and_keeps_exact_lineage():
    admission, _, evaluation = _evaluate()
    assert evaluation.contract_id == RELATION_M1_CONTRACT_ID
    assert evaluation.required_basis_kind == RELATION_BASIS_KIND
    assert evaluation.decision_state.value == "ELIGIBLE"
    assert evaluation.f1 is not None
    assert evaluation.f1["material"]["signature_id"] == SIG_004
    assert admission.ref.as_dict() in evaluation.f1[
        "originating_relation_admission_exact_refs"
    ]
    assert admission.relation_ref.as_dict() in evaluation.f1[
        "originating_field_forge_relation_exact_refs"
    ]
    assert evaluation.f1["lineage_closure_fingerprint"] == semantic_hash(
        {
            "basis_refs": evaluation.f1["provenance_alias_exact_refs"],
            "admission_refs": evaluation.f1[
                "originating_relation_admission_exact_refs"
            ],
            "field_forge_relation_refs": evaluation.f1[
                "originating_field_forge_relation_exact_refs"
            ],
        }
    )
    assert SIG_004 not in EMPIRICAL_M1_SIGS
    assert M1_CONTRACT_ID != RELATION_M1_CONTRACT_ID


def test_positive_relation_m1_reaches_actual_v557_and_v558_with_v554_family_only():
    admission, _, evaluation = _evaluate()
    v557_authority = _m4_auth("V557-GT2")
    terminal = publish_and_resolve_relation_v554_at_current_m4(
        evaluation,
        producer_allowed_uses=("REVIEW",),
        v557_allowed_uses=("REVIEW",),
        requested_resolution_uses=("REVIEW",),
        v557_authority_ref=v557_authority,
        v557_decision_state=V557DecisionState.ALLOW_REVIEW_ONLY,
        producer_rule_bindings=(v557_authority,),
    )
    assert terminal.resolution.receipt.result_state == "RESOLUTION_COMPLETE"
    assert terminal.publication.ref == terminal.repository.publication_bundle_ref
    assert {entry.obj.producer_family for entry in terminal.repository.entries} == {"V554"}
    assert all(
        entry.obj.source_stage == "M1_RELATION_V554_TO_V557"
        for entry in terminal.repository.entries
    )
    assert {resolved.canonical_producer_family for resolved in terminal.resolution.resolved_entries} == {"V554"}

    f1_entries = [
        entry for entry in terminal.repository.entries
        if entry.obj.semantic_class == "F1"
    ]
    assert len(f1_entries) == 1
    f1_payload = f1_entries[0].obj.payload
    assert admission.ref.as_dict() in f1_payload[
        "originating_relation_admission_exact_refs"
    ]
    assert admission.relation_ref.as_dict() in f1_payload[
        "originating_field_forge_relation_exact_refs"
    ]
    assert "V553" not in repr(f1_payload)
    assert all(entry.obj.producer_family not in {"V555", "V556"} for entry in terminal.repository.entries)


def test_admission_ref_hash_loss_fails_closed_even_if_projection_hash_is_recomputed():
    bridge = prepare_typed_d_to_e_relation_basis(
        _admission(), v554_rule_ref=_v554_rule()
    )
    bad = deepcopy(bridge.payload)
    bad["projection"]["relation_admission_ref"]["content_hash"] = _h("wrong-admission")
    bad["projection_hash"] = semantic_hash(bad["projection"])
    prep = prepare_admitted_field_forge_relation_basis(bad)
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE
    assert "relation admission ref mismatch" in prep.reason


def test_authority_version_hash_loss_fails_closed_without_label_fallback():
    bridge = prepare_typed_d_to_e_relation_basis(
        _admission(), v554_rule_ref=_v554_rule()
    )
    bad = deepcopy(bridge.payload)
    bad["projection"]["relation_admission_authority_ref"] = {
        "authority_id": bad["projection"]["relation_admission_authority_ref"][
            "authority_id"
        ],
        "authority_version": "LABEL_ONLY",
        "authority_content_hash": _h("different-authority"),
    }
    bad["projection_hash"] = semantic_hash(bad["projection"])
    prep = prepare_admitted_field_forge_relation_basis(bad)
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE
    assert "admission authority mismatch" in prep.reason


def test_empirical_direct_basis_substitution_is_rejected():
    bridge = prepare_typed_d_to_e_relation_basis(
        _admission(), v554_rule_ref=_v554_rule()
    )
    bad = deepcopy(bridge.payload)
    bad["basis_ref"]["kind"] = "DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION"
    prep = prepare_admitted_field_forge_relation_basis(bad)
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE
    assert "relation basis ref" in prep.reason


def test_v553_coercion_key_is_rejected_on_relation_path():
    bridge = prepare_typed_d_to_e_relation_basis(
        _admission(), v554_rule_ref=_v554_rule()
    )
    bad = deepcopy(bridge.payload)
    bad["v553_object_id"] = "forbidden"
    prep = prepare_admitted_field_forge_relation_basis(bad)
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE
    assert "V553 coercion" in prep.reason


def test_permission_widening_from_d_receipt_is_rejected_before_m1():
    admission = replace(
        _admission(),
        relation_permission_ceiling=("REVIEW_ONLY",),
        target_use_permissions=("STRUCTURAL_MEDIATION_INPUT",),
    )
    with pytest.raises(GT12TypedBridgeError, match="permission widens"):
        prepare_typed_d_to_e_relation_basis(
            admission,
            v554_rule_ref=_v554_rule(),
        )


def test_unknown_or_empirical_m1_contract_cannot_enter_relation_m4_binding():
    _, _, evaluation = _evaluate()
    unknown = replace(evaluation, contract_id="M1_UNKNOWN_CONTRACT@1")
    with pytest.raises(M4IntegrityError):
        structural_objects_from_accepted_m1(
            unknown,
            producer_allowed_uses=("REVIEW",),
        )
    empirical = replace(evaluation, contract_id=M1_CONTRACT_ID)
    with pytest.raises(GT12TypedBridgeError, match="empirical-direct"):
        publish_and_resolve_relation_v554_at_current_m4(
            empirical,
            producer_allowed_uses=("REVIEW",),
            v557_allowed_uses=("REVIEW",),
            requested_resolution_uses=("REVIEW",),
            v557_authority_ref=_m4_auth("EMPIRICAL-SUBSTITUTION"),
            v557_decision_state=V557DecisionState.ALLOW_REVIEW_ONLY,
        )


def test_cross_class_dedup_is_not_available_to_relation_sig004():
    _, _, evaluation = _evaluate()
    assert evaluation.required_basis_kind == RELATION_BASIS_KIND
    assert evaluation.f1["material"]["signature_id"] == SIG_004
    assert SIG_004 not in EMPIRICAL_M1_SIGS
    assert set(EMPIRICAL_M1_SIGS) == {
        "V554-SIG-001-NONTEMPORAL-EXACT",
        "V554-SIG-002-TEMPORAL-POINT-EXACT",
        "V554-SIG-003-TEMPORAL-RELATIONAL-EXACT",
    }


def test_current_v557_permission_widening_still_fails_closed():
    _, _, evaluation = _evaluate()
    with pytest.raises(PermissionWideningError):
        publish_and_resolve_relation_v554_at_current_m4(
            evaluation,
            producer_allowed_uses=("REVIEW",),
            v557_allowed_uses=("CONTEXT",),
            requested_resolution_uses=("CONTEXT",),
            v557_authority_ref=_m4_auth("WIDEN"),
            v557_decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
        )


def test_v558_repository_hash_corruption_is_integrity_failure():
    _, _, evaluation = _evaluate()
    terminal = publish_and_resolve_relation_v554_at_current_m4(
        evaluation,
        producer_allowed_uses=("REVIEW",),
        v557_allowed_uses=("REVIEW",),
        requested_resolution_uses=("REVIEW",),
        v557_authority_ref=_m4_auth("CORRUPTION"),
        v557_decision_state=V557DecisionState.ALLOW_REVIEW_ONLY,
    )
    stale = replace(terminal.repository, repository_hash=_h("stale-repository"))
    query = make_context_query(
        tuple(ContextQueryItem(key, ("REVIEW",)) for key in terminal.resolution_keys)
    )
    with pytest.raises(ClosureIntegrityError, match="repository bundle checksum"):
        resolve_v558(stale, query)


def test_typed_negative_admission_is_not_laundered_into_relation_basis():
    admission = replace(
        _admission(),
        decision=AdmissionDecision.NONCOMPARABLE,
        target_use_permissions=(),
        applicable_negative_denial_noncomparability_refs=(
            _ref("TYPED_NEGATIVE", "noncomparable"),
        ),
    )
    with pytest.raises(GT12TypedBridgeError, match="only positive ADMITTED"):
        prepare_typed_d_to_e_relation_basis(
            admission,
            v554_rule_ref=_v554_rule(),
        )


def test_actor_or_v3_authority_is_not_created_by_bridge_payload():
    bridge = prepare_typed_d_to_e_relation_basis(
        _admission(), v554_rule_ref=_v554_rule()
    )

    authority_ids: list[str] = []
    mapping_keys: list[str] = []

    def walk(value):
        if isinstance(value, dict):
            mapping_keys.extend(str(key) for key in value)
            authority_id = value.get("authority_id")
            if isinstance(authority_id, str):
                authority_ids.append(authority_id)
            for item in value.values():
                walk(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                walk(item)

    walk(bridge.payload)
    assert not any(identifier.startswith("V3") for identifier in authority_ids)
    assert not any("ACTOR" in identifier.upper() for identifier in authority_ids)
    assert not any(key.lower().startswith("actor") for key in mapping_keys)
    assert not any("v3_transition" in key.lower() for key in mapping_keys)
    assert bridge.payload["projection"]["temporal_semantic_disposition"] == (
        "NO_NEW_V553_TEMPORAL_MEANING_REQUIRED"
    )
    assert bridge.payload["focal_structural_proposition_ref"] == (
        FOCAL_STRUCTURAL_PROPOSITION
    )
