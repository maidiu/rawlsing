from __future__ import annotations

from dataclasses import replace
import hashlib

import pytest

from rawlsing_next.m1_temporal_v554_admission_dedup import (
    M1_CONTRACT_ID,
    M1DecisionState,
    SIGS as EMPIRICAL_M1_SIGS,
    TARGET_USE,
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
    RelationPreparationState,
    evaluate_m1_admitted_field_forge_relation_v554,
    make_nonpositive_relation_basis_preparation,
    prepare_admitted_field_forge_relation_basis,
)
from rawlsing_next.m4_m1_evaluation_binding import (
    ACCEPTED_M1_EVALUATION_CONTRACT_IDS,
    structural_objects_from_accepted_m1,
)
from rawlsing_next.m4_v557_v558_publication_repository import M4IntegrityError


def _h(label: str) -> str:
    return hashlib.sha256(label.encode()).hexdigest()


def _ref(kind: str, tag: str) -> dict[str, str]:
    return {
        "kind": kind,
        "object_id": f"urn:test:{kind.lower()}:{tag}",
        "content_hash": _h(f"{kind}:{tag}"),
    }


def _auth(tag: str) -> dict[str, str]:
    return {"id": f"AUTH-{tag}", "version": "1.0.0", "hash": _h(f"auth:{tag}")}


def _rule() -> dict[str, str]:
    return {
        "id": "V554-RULE-GT2-CS",
        "version": "1.0.0",
        "hash": _h("v554-rule-gt2"),
    }


def _admission(
    tag: str = "a",
    *,
    participants=None,
    source_universe: str = "universe:afrobarometer:r5",
) -> dict[str, object]:
    participants = participants or [
        "role:CONDITIONER=Q86B",
        "role:TARGET=Q86A",
        "order:CONDITIONER_THEN_TARGET",
        "cardinality:2",
    ]
    return {
        "schema_id": RELATION_ADMISSION_SCHEMA,
        "field_forge_relation_admission_id": f"prev3-ff-rel-admission:{tag}",
        "field_forge_relation_admission_content_hash": _h(f"admission:{tag}"),
        "field_forge_relation_ref": _ref("FIELD_FORGE_EXACT_RELATION", tag),
        "relation_owner_ref_or_id": "FIELD_FORGE_R2_RELATION_PRODUCER",
        "relation_rule_ref": _auth("FF-CONDITIONAL-SUPPORT"),
        "relation_typed_state": "SUPPORTED",
        "admission_authority_ref": _auth("PREV3-FF-REL-ADMISSION"),
        "admission_rule_ref": _auth("FIELD_FORGE_RELATION_ADMISSION_RULE"),
        "admission_decision_state": "ADMITTED",
        "target_use_ref": TARGET_USE,
        "requested_downstream_owner_or_contract_family": RELATION_M1_CONTRACT_ID,
        "relation_semantic_identity_refs": ["ff:conditional-support@1"],
        "native_scope_identity_refs": ["scope:afrobarometer:r5:riskset"],
        "source_universe_refs": [source_universe],
        "risk_set_refs": ["riskset:first-genuine-canary-common-coexposure@1"],
        "relation_participant_role_order_cardinality_refs": list(participants),
        "target_use_permission_refs": ["permission:STRUCTURAL_MEDIATION_INPUT"],
        "effective_time_or_interval_refs_required_by_target_use": [],
        "estimand_refs": ["estimand:RAW_WITHIN_RISK_SET"],
        "measure_and_weight_authority_refs": [
            "measure:RAW",
            "weight:NOT_APPLICABLE",
        ],
        "source_relation_comparability_authority_refs_where_required": [],
        "applicable_negative_denial_noncomparability_refs": [],
        "interpretation_critical_authority_refs": [
            "authority:CONDITIONER_NOT_CAUSE",
            "authority:TARGET_NOT_EFFECT",
        ],
        "relation_information_loss_declaration": RELATION_INFORMATION_LOSS,
        "producer_replay_locator_or_reference_root": f"replay:ff-admission:{tag}",
        "authority_current_selection_dependency_provenance_refs": [
            "current:ff-relation",
            "current:relation-admission-rule",
            "dependency:gt2-joint-fact",
        ],
    }


def _projection(
    admission: dict[str, object],
    *,
    temporal=None,
) -> dict[str, object]:
    temporal = temporal or RELATION_TEMPORAL_DISPOSITION
    return {
        "relation_admission_ref": {
            "kind": RELATION_ADMISSION_REF_KIND,
            "object_id": admission["field_forge_relation_admission_id"],
            "content_hash": admission["field_forge_relation_admission_content_hash"],
        },
        "relation_admission_authority_ref": admission["admission_authority_ref"],
        "relation_admission_rule_ref": admission["admission_rule_ref"],
        "relation_admission_decision_state": "ADMITTED",
        "field_forge_relation_ref": admission["field_forge_relation_ref"],
        "relation_semantic_identity_refs": list(
            admission["relation_semantic_identity_refs"]
        ),
        "relation_participant_role_order_cardinality_refs": list(
            admission["relation_participant_role_order_cardinality_refs"]
        ),
        "focal_structural_proposition_ref": "prop:GT2:Q86B_CONDITIONS_Q86A_SUPPORT",
        "native_scope_identity_refs": list(admission["native_scope_identity_refs"]),
        "source_universe_refs": list(admission["source_universe_refs"]),
        "risk_set_refs": list(admission["risk_set_refs"]),
        "target_use_ref": TARGET_USE,
        "requested_downstream_owner_or_contract_family": RELATION_M1_CONTRACT_ID,
        "target_use_permission_refs": list(admission["target_use_permission_refs"]),
        "effective_time_or_interval_refs_required_by_target_use": [],
        "estimand_refs": list(admission["estimand_refs"]),
        "measure_and_weight_authority_refs": list(
            admission["measure_and_weight_authority_refs"]
        ),
        "source_relation_comparability_authority_refs_where_required": [],
        "applicable_negative_denial_noncomparability_refs": [],
        "interpretation_critical_authority_refs": list(
            admission["interpretation_critical_authority_refs"]
        ),
        "producer_replay_locator_or_reference_root": admission[
            "producer_replay_locator_or_reference_root"
        ],
        "authority_current_selection_dependency_provenance_refs": list(
            admission["authority_current_selection_dependency_provenance_refs"]
        ),
        "information_loss_declaration": RELATION_INFORMATION_LOSS,
        "temporal_semantic_disposition": temporal,
    }


def _eq(projection: dict[str, object]) -> dict[str, object]:
    return {
        "focal_structural_proposition_ref": projection[
            "focal_structural_proposition_ref"
        ],
        "target_use": TARGET_USE,
        "v554_rule_id": _rule()["id"],
        "v554_rule_version": _rule()["version"],
        "v554_rule_hash": _rule()["hash"],
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
            list(projection["source_universe_refs"])
        ),
        "estimand_fingerprint": semantic_hash(list(projection["estimand_refs"])),
        "measure_and_weight_authority_fingerprint": semantic_hash(
            list(projection["measure_and_weight_authority_refs"])
        ),
        "rule_relevant_source_relation_comparability_authority_fingerprint": semantic_hash(
            list(
                projection[
                    "source_relation_comparability_authority_refs_where_required"
                ]
            )
        ),
        "interpretation_critical_semantic_authority_fingerprint": semantic_hash(
            list(projection["interpretation_critical_authority_refs"])
        ),
    }


def _prep(
    tag="a",
    *,
    participants=None,
    source_universe="universe:afrobarometer:r5",
    temporal=None,
):
    admission = _admission(
        tag,
        participants=participants,
        source_universe=source_universe,
    )
    projection = _projection(admission, temporal=temporal)
    payload = {
        "relation_admission": admission,
        "basis_ref": {
            "kind": RELATION_BASIS_KIND,
            "object_id": admission["field_forge_relation_admission_id"],
            "content_hash": admission["field_forge_relation_admission_content_hash"],
        },
        "projection": projection,
        "projection_hash": semantic_hash(projection),
        "equivalence_key": _eq(projection),
        "selected_rule_relevant_basis_semantics": {
            "relation_family": "EXACT_CONDITIONAL_SUPPORT_PROFILE_WITHIN_SCOPE@1.0.0",
            "conditioner": "Q86B",
            "target": "Q86A",
            "count_profile_only": True,
        },
        "focal_structural_proposition_ref": projection[
            "focal_structural_proposition_ref"
        ],
    }
    return prepare_admitted_field_forge_relation_basis(payload)


def _publication(use="use:GT2") -> dict[str, object]:
    return {
        "authority_id": "V557-PUBLISH-GT2",
        "authority_version": "1.0.0",
        "authority_hash": _h("publish:gt2"),
        "producer": "V554",
        "publisher": "V557",
        "governed_use_id": use,
        "rule_ref": _rule(),
        "decision": "AUTHORIZED",
        "allowed_object_families": ["F1", "F2", "B1"],
    }


def _evaluate(preps, *, use="use:GT2"):
    return evaluate_m1_admitted_field_forge_relation_v554(
        governed_use_id=use,
        v554_rule_ref=_rule(),
        focal_structural_proposition_ref="prop:GT2:Q86B_CONDITIONS_Q86A_SUPPORT",
        preparations=preps,
        required_authority_snapshot_refs=["snapshot:gt2"],
        authority_bundle_material={
            "relation_admission_contract": RELATION_ADMISSION_SCHEMA,
            "v554": "1.0.0",
        },
        producer_reference_spine_fingerprint="spine:gt2",
        publication_authority=_publication(use),
    )


def test_exact_admitted_relation_sig004_emits_one_f1_and_direct_handoff():
    prep = _prep()
    assert prep.state is RelationPreparationState.RELATION_BASIS_READY
    result = _evaluate([prep])

    assert result.contract_id == RELATION_M1_CONTRACT_ID
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.required_basis_kind == RELATION_BASIS_KIND
    assert result.support_count == 1
    assert result.f1 is not None
    assert result.f1["material"]["signature_id"] == SIG_004
    assert result.b1 is not None
    assert result.direct_v557_handoff["route"] == "V554_TO_V557_DIRECT"


def test_exact_same_relation_semantics_dedup_aliases_within_relation_class_only():
    a = _prep("a")
    b = _prep("b")
    b_candidate = dict(b.candidate)
    b_candidate["equivalence_key"] = dict(a.candidate["equivalence_key"])
    b_candidate["selected_rule_relevant_basis_semantics"] = dict(
        a.candidate["selected_rule_relevant_basis_semantics"]
    )
    b = replace(b, candidate=b_candidate)

    result = _evaluate([b, a])
    assert result.decision_state is M1DecisionState.ELIGIBLE
    assert result.support_count == 1
    assert result.f1["provenance_alias_refs"] == [
        "prev3-ff-rel-admission:a",
        "prev3-ff-rel-admission:b",
    ]


def test_role_order_change_is_distinct_basis_group_and_no_winner_is_selected():
    a = _prep("a")
    swapped = [
        "role:CONDITIONER=Q86A",
        "role:TARGET=Q86B",
        "order:CONDITIONER_THEN_TARGET",
        "cardinality:2",
    ]
    b = _prep("b", participants=swapped)
    result = _evaluate([a, b])
    assert (
        result.decision_state
        is M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY
    )
    assert result.f1 is None
    assert result.support_count == 0


def test_source_universe_difference_is_not_deduplicated_or_arbitrarily_selected():
    a = _prep("a")
    b = _prep("b", source_universe="universe:other")
    result = _evaluate([a, b])
    assert (
        result.decision_state
        is M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY
    )
    assert result.f1 is None


def test_missing_relation_lineage_identity_fails_closed_during_preparation():
    admission = _admission("bad")
    projection = _projection(admission)
    eq = _eq(projection)
    del eq["originating_admitted_relation_lineage_fingerprint"]
    prep = prepare_admitted_field_forge_relation_basis(
        {
            "relation_admission": admission,
            "basis_ref": {
                "kind": RELATION_BASIS_KIND,
                "object_id": admission["field_forge_relation_admission_id"],
                "content_hash": admission[
                    "field_forge_relation_admission_content_hash"
                ],
            },
            "projection": projection,
            "projection_hash": semantic_hash(projection),
            "equivalence_key": eq,
            "selected_rule_relevant_basis_semantics": {"x": "y"},
            "focal_structural_proposition_ref": projection[
                "focal_structural_proposition_ref"
            ],
        }
    )
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE
    assert prep.candidate is None


def test_temporalization_required_is_typed_and_never_fabricates_v553():
    prep = _prep("time", temporal="REQUIRES_V553_OWNED_TEMPORAL_MEANING")
    assert prep.state is RelationPreparationState.TEMPORALIZATION_REQUIRED
    assert prep.candidate is None
    assert "V553" in prep.reason


@pytest.mark.parametrize(
    ("state", "expected"),
    [
        (
            RelationPreparationState.DENIED,
            M1DecisionState.INELIGIBLE_EXPLICIT_DENIAL,
        ),
        (
            RelationPreparationState.NONCOMPARABLE,
            M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY,
        ),
        (
            RelationPreparationState.DEFERRED_MISSING_AUTHORITY,
            M1DecisionState.INELIGIBLE_MISSING_REQUIRED_AUTHORITY,
        ),
    ],
)
def test_nonpositive_preparation_is_not_laundered_into_valid_empty(state, expected):
    blocked = make_nonpositive_relation_basis_preparation(
        state, f"blocked:{state.value}"
    )
    result = _evaluate([blocked])
    assert blocked.state is state
    assert result.decision_state is expected
    assert result.decision_state is not M1DecisionState.VALID_EMPTY
    assert state.value in result.reason


def test_true_valid_empty_preparation_may_remain_m1_valid_empty_without_filler():
    empty = make_nonpositive_relation_basis_preparation(
        RelationPreparationState.VALID_EMPTY,
        "upstream relation admission was lawfully valid-empty",
    )
    result = _evaluate([empty])
    assert result.decision_state is M1DecisionState.VALID_EMPTY
    assert result.f1 is None
    assert result.support_count == 0


def test_structural_empirical_and_v553_coercion_keys_are_rejected():
    admission = _admission("coerce")
    projection = _projection(admission)
    payload = {
        "relation_admission": admission,
        "basis_ref": {
            "kind": RELATION_BASIS_KIND,
            "object_id": admission["field_forge_relation_admission_id"],
            "content_hash": admission["field_forge_relation_admission_content_hash"],
        },
        "projection": projection,
        "projection_hash": semantic_hash(projection),
        "equivalence_key": _eq(projection),
        "selected_rule_relevant_basis_semantics": {"x": "y"},
        "focal_structural_proposition_ref": projection[
            "focal_structural_proposition_ref"
        ],
        "v553_object_id": "forbidden",
    }
    prep = prepare_admitted_field_forge_relation_basis(payload)
    assert prep.state is RelationPreparationState.INTEGRITY_FAILURE
    assert "forbidden empirical/V553 coercion" in prep.reason


def test_empirical_m1_contract_and_signature_registry_remain_unchanged():
    assert M1_CONTRACT_ID == "M1_TEMPORAL_V554_INGRESS_SEAM@1.0.0"
    assert SIG_004 not in EMPIRICAL_M1_SIGS
    assert EMPIRICAL_M1_SIGS == {
        "V554-SIG-001-NONTEMPORAL-EXACT",
        "V554-SIG-002-TEMPORAL-POINT-EXACT",
        "V554-SIG-003-TEMPORAL-RELATIONAL-EXACT",
    }


def test_m4_binding_rejects_caller_minted_relation_producer_uses():
    result = _evaluate([_prep("m4")])
    with pytest.raises(M4IntegrityError, match="caller-selected"):
        structural_objects_from_accepted_m1(
            result,
            producer_allowed_uses=["REVIEW", "CONTEXT"],
        )

def test_m4_binding_rejects_unknown_m1_contract_and_acceptance_set_is_exact():
    result = _evaluate([_prep("unknown")])
    bad = replace(result, contract_id="M1_UNKNOWN_CONTRACT@1")
    with pytest.raises(M4IntegrityError):
        structural_objects_from_accepted_m1(
            bad,
            producer_allowed_uses=["REVIEW"],
        )
    assert ACCEPTED_M1_EVALUATION_CONTRACT_IDS == {
        M1_CONTRACT_ID,
        RELATION_M1_CONTRACT_ID,
    }
