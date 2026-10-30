"""Retained GT2 -> N10E analytical preparation court (H03).

This court proves the exact retained preparation and the exact contract gap. It
does not manufacture a positive N10E receipt, synthetic respondent preimages,
model authority, pairing authority or probability geometry.
"""
from __future__ import annotations

import inspect
import json
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace

import pytest

import rawlsing_next.pre553_analytical_composition as composition
import rawlsing_next.pre553_empirical_possibility_provider as provider
import rawlsing_next.pre553_repo_native_current_payload as current
import rawlsing_next.wave1_gt12_i03_positive_facts as gt12b
from rawlsing_next.field_forge_conditional_support import (
    FieldForgeConditionalSupportError,
    produce_exact_conditional_support_profile,
)
from rawlsing_next.pre553_empirical_objects import canonicalize, exact_ref
from rawlsing_next.pre553_retained_gt2_analytical_preparation import (
    DETERMINANT_ABSENT_TRANSPORT,
    DETERMINANT_EXACT_RECONSTRUCTED,
    DETERMINANT_EXACT_RETAINED,
    DETERMINANT_UNAVAILABLE_AUTHORITY,
    PREPARATION_CONTRACT_ID,
    PREPARATION_STATE,
    RetainedGT2AnalyticalPreparationError,
    RetainedGT2N10EContractGapError,
    load_retained_gt2_analytical_preparation,
)

ROOT = Path(__file__).resolve().parents[2]
HQ230 = ROOT / "PYAT_CONTROL_ROOM" / "C1_AT07_OWNER_NATIVE_MODEL_AUTHORITY_HQ230_R1"
REAL_ANCHORS = {
    ("0", "0"): 2112,
    ("0", "1"): 4493,
    ("1", "0"): 491,
    ("1", "1"): 11232,
    ("DK", "1"): 250,
    ("DK", "DK"): 334,
    ("MISSING", "1"): 9,
    ("MISSING", "MISSING"): 6,
}
EXPECTED_CONDITIONER_DENOMINATORS = (6784, 11787, 624, 0, 0, 15)


def _state(value):
    if isinstance(value, str):
        return value
    return value["typed_response_state"]


@pytest.fixture(scope="module")
def prepared():
    return load_retained_gt2_analytical_preparation()


def _determinant(prepared, name):
    matches = [item for item in prepared.determinants if item.name == name]
    assert len(matches) == 1
    return matches[0]


def _retained_query_fact():
    return current.load_current_gt2_query_fact_from_committed_transport()


def _new_query(query, **overrides):
    fields = dict(query.semantic_fields)
    fields.update(overrides)
    return type(query)(
        typed_state=query.typed_state,
        authority_snapshot_refs=query.authority_snapshot_refs,
        dependency_refs=query.dependency_refs,
        producer_replay_locator_or_reference_root=(
            query.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


def _new_fact(fact, **overrides):
    fields = dict(fact.semantic_fields)
    fields.update(overrides)
    return type(fact)(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=(
            fact.producer_replay_locator_or_reference_root
        ),
        **fields,
    )


# --------------------------------------------------------------------------
# Positive preparation: exact retained input, no new probability model
# --------------------------------------------------------------------------
def test_preparation_identity_and_retained_refs_are_exact(prepared):
    query, fact = _retained_query_fact()
    assert prepared.schema == PREPARATION_CONTRACT_ID
    assert prepared.preparation_state == PREPARATION_STATE
    assert prepared.query_ref == query.ref
    assert prepared.fact_ref == fact.ref
    assert prepared.replay_ref == exact_ref(fact.replay_ref)
    assert prepared.risk_set_ref == exact_ref(query.risk_set_ref)
    assert prepared.universe_ref == exact_ref(query.empirical_universe_refs[0])
    assert prepared.predicate_hash == current.CURRENT_PREDICATE_HASH
    assert prepared.release_ref.object_id == "R5_GT12_Q86A_Q86B_FROZEN"
    assert prepared.release_ref.content_hash == (
        "8315b104a94ae985a3ee3d77c8c365d5fcef6b6cb51a606df5bf141434668295"
    )
    assert prepared.relation_ref.content_hash == (
        "1ffdfe536adc01d35709521145b9c8057f589c20983f507d5ed6197c4ad27d19"
    )


def test_exact_predicate_is_reconstructed_but_is_not_value_bearing(prepared):
    query, fact = _retained_query_fact()
    predicate = gt12b.reconstruct_gt2_risk_cohort_predicate(query=query, fact=fact)
    assert predicate.ref == prepared.predicate_ref
    assert predicate.content_hash == current.CURRENT_PREDICATE_HASH
    assert prepared.predicate_leaf_type == "DERIVED_BRANCH_COHORT"
    assert prepared.predicate_value_bearing_leaf_count == 0
    assert composition._actual_leaves(predicate) == []


def test_joint_geometry_preserves_complete_6x6_and_real_anchors(prepared):
    assert len(prepared.joint_cells) == 36
    assert (
        sum(int(cell["raw_numerator_support"]) for cell in prepared.joint_cells)
        == 19_210
    )
    seen = {}
    zeros = 0
    for cell in prepared.joint_cells:
        left, right = cell["cell"]
        seen[(_state(left), _state(right))] = int(
            cell["raw_numerator_support"]
        )
        if int(cell["raw_numerator_support"]) == 0:
            zeros += 1
    assert zeros == 23
    for key, count in REAL_ANCHORS.items():
        assert seen[key] == count


def test_conditioned_rows_preserve_direction_denominators_zeros_and_minorities(prepared):
    rows = prepared.conditioned_rows
    assert tuple(row.conditioner_denominator_support for row in rows) == (
        EXPECTED_CONDITIONER_DENOMINATORS
    )
    assert tuple(_state(row.conditioner_state) for row in rows) == (
        "0",
        "1",
        "DK",
        "NOT_ASKED",
        "REFUSAL",
        "MISSING",
    )
    assert sum(row.conditioner_denominator_support for row in rows) == 19_210
    for row in rows:
        assert len(row.target_counts) == 6
        assert sum(
            int(count["joint_support_count"]) for count in row.target_counts
        ) == row.conditioner_denominator_support
        assert tuple(_state(count["target_state"]) for count in row.target_counts) == (
            "0",
            "1",
            "DK",
            "NOT_ASKED",
            "REFUSAL",
            "MISSING",
        )

    q86b_one = rows[1]
    counts = {
        _state(count["target_state"]): int(count["joint_support_count"])
        for count in q86b_one.target_counts
    }
    assert counts == {
        "0": 491,
        "1": 11232,
        "DK": 63,
        "NOT_ASKED": 0,
        "REFUSAL": 0,
        "MISSING": 1,
    }
    assert q86b_one.conditioner_denominator_support == 11787
    assert rows[3].conditioner_denominator_support == 0
    assert rows[4].conditioner_denominator_support == 0
    assert rows[5].conditioner_denominator_support == 15


# --------------------------------------------------------------------------
# Exact N10E determinant analysis: exact vs typed-null
# --------------------------------------------------------------------------
def test_provider_shape_exposes_exact_fields_and_no_geometry_channel(prepared):
    shape = prepared.provider_request_shape()
    assert shape["provider_callable"].endswith("provide_empirical_possibility_slice")
    assert shape["empirical_query"] == prepared.query_ref.as_dict()
    assert shape["predicate"]["ref"] == prepared.predicate_ref.as_dict()
    assert shape["predicate"]["value_bearing_leaf_count"] == 0
    assert shape["release_refs"] == [prepared.release_ref.as_dict()]
    assert shape["repository"] is None
    assert shape["authority_registry"] is None
    assert shape["consumer_query"] is None
    assert shape["model_rule"] is None
    assert shape["condition_binding_witness"] is None
    assert "geometry" not in shape
    assert "probability" not in shape
    assert "evidence" not in shape


def test_exact_determinants_are_marked_exact_and_blockers_are_typed(prepared):
    query = _determinant(prepared, "empirical_query")
    predicate = _determinant(prepared, "predicate")
    assert query.state == DETERMINANT_EXACT_RETAINED
    assert predicate.state == DETERMINANT_EXACT_RECONSTRUCTED
    assert predicate.ref_or_null["content_hash"] == current.CURRENT_PREDICATE_HASH

    assert _determinant(prepared, "repository").state == (
        DETERMINANT_ABSENT_TRANSPORT
    )
    assert _determinant(prepared, "authority_registry").state == (
        DETERMINANT_ABSENT_TRANSPORT
    )
    assert _determinant(prepared, "release_refs").state == (
        DETERMINANT_ABSENT_TRANSPORT
    )
    for name in (
        "consumer_query",
        "model_rule",
        "condition_binding_witness",
    ):
        assert _determinant(prepared, name).state == (
            DETERMINANT_UNAVAILABLE_AUTHORITY
        )


def test_require_n10e_provider_route_refuses_with_exact_missing_set(prepared):
    with pytest.raises(RetainedGT2N10EContractGapError) as excinfo:
        prepared.require_n10e_provider_route()
    assert [name for name, _ in excinfo.value.missing] == [
        "repository",
        "authority_registry",
        "release_refs",
        "consumer_query",
        "model_rule",
        "condition_binding_witness",
    ]
    assert "N10E_RETAINED_CONTRACT_GAP" in str(excinfo.value)


def test_preparation_cannot_claim_provider_or_consumer_or_replay(prepared):
    with pytest.raises(RetainedGT2AnalyticalPreparationError):
        replace(prepared, provider_receipt_or_null={"fake": True})
    with pytest.raises(RetainedGT2AnalyticalPreparationError):
        replace(prepared, consumer_result_or_null={"fake": True})
    with pytest.raises(RetainedGT2AnalyticalPreparationError):
        replace(prepared, replay_or_null={"fake": True})


def test_preparation_is_deterministic_and_content_addressed(prepared):
    second = load_retained_gt2_analytical_preparation()
    assert second.material() == prepared.material()
    assert second.preparation_ref == prepared.preparation_ref
    assert prepared.preparation_ref.content_hash == prepared.preparation_hash
    assert prepared.preparation_ref.object_id.endswith(
        prepared.preparation_hash
    )


# --------------------------------------------------------------------------
# Contract mismatch and hostile negatives
# --------------------------------------------------------------------------
def test_accepted_n10e_direct_route_re_executes_i03_and_has_no_fact_input(prepared):
    compose_params = set(
        inspect.signature(
            composition.compose_positioned_subject_possibility
        ).parameters
    )
    provider_params = set(
        inspect.signature(provider.provide_empirical_possibility_slice).parameters
    )
    assert "repository" in compose_params
    assert "repository" in provider_params
    for forbidden in ("fact", "retained_fact", "executed_fact", "producer_result"):
        assert forbidden not in compose_params
        assert forbidden not in provider_params
    assert "execute_empirical_query(" in inspect.getsource(
        composition.compose_positioned_subject_possibility
    )


def test_direct_grain_rejects_q86a_consumer_against_q86b_first_target(prepared):
    query, _ = _retained_query_fact()
    consumer_view = SimpleNamespace(
        source_universe_ref=prepared.universe_ref,
        release_ref=prepared.release_ref,
        target_ref=exact_ref(query.target_refs[1]),
    )
    with pytest.raises(
        composition.AnalyticalCompositionError,
        match="TARGET_TOPOLOGY_OR_DOMAIN_MISMATCH",
    ):
        composition._validate_direct_grain(
            empirical_query=query,
            consumer_query=consumer_view,
            release_refs=(prepared.release_ref,),
        )


def test_reverse_field_forge_conditioning_is_rejected(prepared):
    query, fact = _retained_query_fact()
    with pytest.raises(
        FieldForgeConditionalSupportError, match="target role/order"
    ):
        produce_exact_conditional_support_profile(
            joint_fact=fact,
            joint_query=query,
            conditioner_ref=query.target_refs[1],
            target_ref=query.target_refs[0],
            producer_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
            relation_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
        )


def test_tampered_joint_count_fails_closed(prepared):
    query, fact = _retained_query_fact()
    tampered_topology = canonicalize(fact.target_topology)
    cells = [
        dict(cell)
        for cell in tampered_topology["complete_cell_semantic_projection"]
    ]
    cells[0]["raw_numerator_support"] += 1
    tampered_topology["complete_cell_semantic_projection"] = cells
    tampered = _new_fact(fact, target_topology=tampered_topology)
    assert tampered.ref != fact.ref
    with pytest.raises(
        FieldForgeConditionalSupportError,
        match="joint cell counts do not equal producer raw numerator support",
    ):
        produce_exact_conditional_support_profile(
            joint_fact=tampered,
            joint_query=query,
            conditioner_ref=query.target_refs[0],
            target_ref=query.target_refs[1],
            producer_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
            relation_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
        )


def test_incomplete_native_cell_set_fails_closed(prepared):
    query, fact = _retained_query_fact()
    incomplete_topology = canonicalize(fact.target_topology)
    incomplete_topology["complete_cell_semantic_projection"] = (
        incomplete_topology["complete_cell_semantic_projection"][:-1]
    )
    incomplete = _new_fact(fact, target_topology=incomplete_topology)
    with pytest.raises(FieldForgeConditionalSupportError):
        produce_exact_conditional_support_profile(
            joint_fact=incomplete,
            joint_query=query,
            conditioner_ref=query.target_refs[0],
            target_ref=query.target_refs[1],
            producer_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
            relation_permission_ceiling=("STRUCTURAL_MEDIATION_INPUT",),
        )


def test_wrong_query_or_risk_identity_is_rejected_by_predicate_reconstruction(prepared):
    query, fact = _retained_query_fact()
    wrong_risk = _new_query(
        query,
        risk_set_ref={
            "kind": "RISK_SET",
            "object_id": "WRONG_RISK",
            "content_hash": "0" * 64,
        },
    )
    with pytest.raises(gt12b.GT12BI03BindingError, match="does not bind"):
        gt12b.reconstruct_gt2_risk_cohort_predicate(query=wrong_risk, fact=fact)

    swapped = _new_query(
        query,
        target_refs=tuple(reversed(tuple(query.target_refs))),
    )
    with pytest.raises(gt12b.GT12BI03BindingError, match="does not bind"):
        gt12b.reconstruct_gt2_risk_cohort_predicate(query=swapped, fact=fact)


def test_retained_transport_does_not_contain_release_objects_or_respondent_preimages():
    manifest_bytes, payloads = current._read_committed_transport()
    manifest = json.loads(manifest_bytes)
    assert manifest["forbidden_material"] == {
        "e2b_execution": False,
        "raw_respondent_response_values": False,
        "sav": False,
        "source_rows": False,
    }
    release = manifest["release"]
    assert set(release) == {"ref", "replay_manifest_ref", "internal_records", "public_objects"}
    assert release["internal_records"] == 19212
    assert release["public_objects"] == 96057
    assert "public_objects_body" not in manifest
    assert "internal_records_body" not in manifest
    assert set(payloads) == {"respondent_refs", "routing_refs", "event_refs"}
    for spec in current._BINARY_SPECS.values():
        assert spec["bytes"] % 32 == 0


def test_structural_field_forge_permission_is_not_an_n10e_model_authority(prepared):
    _, fact = _retained_query_fact()
    authority_ids = {
        ref.authority_id for ref in fact.authority_snapshot_refs
    }
    assert not any(
        "POSITIONED-SUBJECT" in authority_id
        or "WALKBACK" in authority_id
        or "MODEL-RULE" in authority_id
        for authority_id in authority_ids
    )
    assert _determinant(prepared, "model_rule").state == (
        DETERMINANT_UNAVAILABLE_AUTHORITY
    )


def test_hq230_model_authority_is_only_a_candidate_and_is_at07_scoped(prepared):
    proposal = (HQ230 / "01_IDENTITY_AND_SUCCESSION.json").read_text(
        encoding="utf-8"
    )
    snapshot = json.loads(
        (HQ230 / "03_CANONICAL_SNAPSHOT_BODY.json").read_text(encoding="utf-8")
    )
    assert '"status": "CANDIDATE_NOT_ADOPTED"' in proposal
    assert snapshot["status"] == "CANDIDATE_NOT_ADOPTED"
    scope = snapshot["authority_material"]["scope_envelope"]
    assert scope["fixture_ids"] == ["AT07_BIDIRECTIONAL_100"]
    assert scope["real_source_effect"] is False
    assert "GT2" not in json.dumps(scope)
    assert _determinant(prepared, "model_rule").state == (
        DETERMINANT_UNAVAILABLE_AUTHORITY
    )
