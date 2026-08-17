from __future__ import annotations

import copy
import json

import pytest

from data.ddm_build_copy.tests.vozhd_dva_wave0.vertical_continuity import (
    CURRENT_PRODUCTION_COVERAGE,
    ID_FIELDS,
    PRODUCER_OBLIGATIONS,
    SLICE_IDS,
    STAGES,
    ForbiddenInferenceError,
    SemanticContinuityError,
    artifact_shape_report,
    assert_semantic_continuity,
    build_reference_chain,
    build_reference_fixture,
    reject_direct_persona_inference,
    semantic_continuity_report,
)


def _all_ids(value, key: str) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        if key in value and isinstance(value[key], str):
            found.append(value[key])
        for child in value.values():
            found.extend(_all_ids(child, key))
    elif isinstance(value, list):
        for child in value:
            found.extend(_all_ids(child, key))
    return found


def test_fixture_is_deterministic_and_ids_are_unique() -> None:
    left = build_reference_fixture()
    right = build_reference_fixture()
    assert json.dumps(left, sort_keys=True) == json.dumps(right, sort_keys=True)
    assert left["source_identity"]["waves"] == ["W1", "W2", "W3"]
    for key in ID_FIELDS:
        values = _all_ids(left["semantic_payload"], key)
        assert len(values) == len(set(values)), f"duplicate stable IDs for {key}: {values}"


def test_reference_packets_name_future_producer_obligations() -> None:
    chain = build_reference_chain()
    for stage in STAGES:
        packet = chain[stage]
        assert packet["packet_kind"] == "REFERENCE_CONTRACT_FIXTURE_NOT_PRODUCTION_OUTPUT"
        assert packet["production_semantic_readiness_claim"] is False
        assert packet["future_producer_obligation"] == PRODUCER_OBLIGATIONS[stage]


def test_vs1_temporal_persistence_drift_rupture_survives_reference_chain() -> None:
    chain = build_reference_chain()
    for stage in STAGES:
        relations = chain[stage]["semantic_payload"]["temporal_relations"]
        assert {row["trajectory_kind"] for row in relations} == {"PERSISTENT", "DRIFT", "RUPTURE_CANDIDATE"}
        rupture = next(row for row in relations if row["trajectory_kind"] == "RUPTURE_CANDIDATE")
        assert rupture["rupture_claim"]["status"] == "CANDIDATE_ONLY"
        assert rupture["rupture_claim"]["external_event_claim_made"] is False
    assert_semantic_continuity(chain)


def test_vs2_conflicting_pressures_remain_distinct() -> None:
    chain = build_reference_chain()
    for stage in STAGES:
        pressures = chain[stage]["semantic_payload"]["structural_pressures"]
        conflict = [row for row in pressures if row["conflict_set_id"] == "conflict.household-orientation"]
        assert {row["pressure_id"] for row in conflict} == {
            "pressure.local-solidarity",
            "pressure.institutional-discipline",
        }
        assert {row["direction"] for row in conflict} == {-1, 1}


def test_vs3_mediation_buffer_and_amplify_survive_reference_chain() -> None:
    chain = build_reference_chain()
    for stage in STAGES:
        route = chain[stage]["semantic_payload"]["mediation_routes"][0]
        assert route["source_pressure_ids"] == ["pressure.local-solidarity", "pressure.institutional-discipline"]
        assert {row["effect_kind"] for row in route["conditions"]} == {"BUFFER", "AMPLIFY"}


def test_vs4_pressureflow_and_attractor_prerequisites_survive_reference_chain() -> None:
    chain = build_reference_chain()
    for stage in STAGES:
        payload = chain[stage]["semantic_payload"]
        assert {row["route_kind"] for row in payload["pressureflow_routes"]} == {
            "DEFLECTION_CANDIDATE",
            "REINFORCEMENT_CANDIDATE",
        }
        assert len(payload["attractor_prerequisites"]) == 2
        assert all(row["finished_type_assignment_allowed"] is False for row in payload["attractor_prerequisites"])


def test_vs5_uncertainty_absence_and_noncomparability_are_not_zero() -> None:
    chain = build_reference_chain()
    for stage in STAGES:
        epistemic = chain[stage]["semantic_payload"]["epistemic_boundaries"]
        assert epistemic["uncertainty"][0]["state"] == "UNCERTAIN"
        assert epistemic["absence"][0]["state"] == "ABSENT"
        assert epistemic["absence"][0]["numeric_value"] is None
        assert epistemic["noncomparability"][0]["state"] == "NONCOMPARABLE"
        assert epistemic["noncomparability"][0]["numeric_value"] is None


def test_artifact_shape_success_does_not_imply_semantic_readiness() -> None:
    chain = build_reference_chain()
    broken = copy.deepcopy(chain)
    broken["v557"]["semantic_payload"]["epistemic_boundaries"]["noncomparability"] = []
    assert artifact_shape_report(broken)["ready"] is True
    semantic = semantic_continuity_report(broken)
    assert semantic["ready"] is False
    assert semantic["level"] == "semantic_chain"
    assert any("noncomparability" in error for error in semantic["errors"])


def test_information_loss_detector_fails_when_buffer_condition_is_dropped() -> None:
    chain = build_reference_chain()
    broken = copy.deepcopy(chain)
    conditions = broken["v556"]["semantic_payload"]["mediation_routes"][0]["conditions"]
    broken["v556"]["semantic_payload"]["mediation_routes"][0]["conditions"] = [
        row for row in conditions if row["effect_kind"] != "BUFFER"
    ]
    assert artifact_shape_report(broken)["ready"] is True
    with pytest.raises(SemanticContinuityError, match=r"v556: mediation buffer/amplify distinction lost"):
        assert_semantic_continuity(broken)


def test_forbidden_direct_persona_inference_fails_closed() -> None:
    fixture = build_reference_fixture()
    case = fixture["adversarial_cases"][0]
    with pytest.raises(ForbiddenInferenceError, match="fail closed"):
        reject_direct_persona_inference(case)


def test_stage_output_persona_leak_fails_closed() -> None:
    chain = build_reference_chain()
    broken = copy.deepcopy(chain)
    broken["v558"]["generated_outputs"] = {"persona_fact": "invented direct personhood"}
    with pytest.raises(SemanticContinuityError, match=r"v558: forbidden direct personhood output"):
        assert_semantic_continuity(broken)


def test_full_reference_consumer_contract_is_semantically_ready() -> None:
    chain = build_reference_chain()
    assert artifact_shape_report(chain)["ready"] is True
    semantic = semantic_continuity_report(chain)
    assert semantic["ready"] is True
    assert semantic["reference_contract_only"] is True
    assert semantic["production_semantic_readiness_claim"] is False


@pytest.mark.parametrize("slice_id", sorted(SLICE_IDS))
@pytest.mark.xfail(strict=True, reason="Wave-0 expected contract gap: current production V553-V558 does not yet preserve this slice end-to-end")
def test_current_production_slice_is_explicit_gap(slice_id: str) -> None:
    gap = CURRENT_PRODUCTION_COVERAGE[slice_id]
    assert gap["future_producer_obligation"]
    assert gap["first_gap"]
    # Desired future condition. Strict XFAIL keeps semantic debt visible without
    # pretending that artifact/process success is semantic success.
    assert gap["status"] == "PASS", gap["reason"]
