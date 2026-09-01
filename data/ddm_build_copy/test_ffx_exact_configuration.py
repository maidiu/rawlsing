from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from data.ddm_build_copy import ddm_ffx_exact_configuration as m
from data.ddm_build_copy import field_forge_ffx002_harness as harness
from data.ddm_build_copy.compile_ffx_exact_configuration import main as cli_main


def _manifest():
    manifest = {
        "manifest_schema_version": harness.SCHEMA_VERSION,
        "current_execution_sha": "a" * 40,
        "observation_substrate_ref": {"ref": "synthetic-observations", "hash": "obs-hash"},
        "respondent_entity_binding_ref": {"ref": "synthetic-unit-binding"},
        "exposure_risk_set_ref": {"ref": "synthetic-exposure"},
        "source_scope_ref": {"source": "SYNTHETIC", "wave": "R1"},
        "source_native_measurement_refs": [{"id": "P1"}, {"id": "P2"}, {"id": "D1"}, {"id": "D2"}, {"id": "D3"}],
        "qimpl_measurement_binding_refs": [{"id": "QP1"}, {"id": "QP2"}, {"id": "QD1"}, {"id": "QD2"}, {"id": "QD3"}],
        "response_state_semantics_ref": {"ref": "opaque-frozen-state-ids"},
        "special_state_semantics_ref": {"ref": "synthetic-special-states"},
        "ttar_execution_sequence": "NONE",
        "post_transform_state_manifest": {"ref": "synthetic-frozen-state-manifest"},
        "claim_scope_ref": "SYNTHETIC_CANARY",
        "estimand_ref": "SYNTHETIC_SAMPLE_DESCRIPTIVE",
        "weight_design_refs": "NONE",
        "analytic_role_authority_refs": [{"id": "PRA-SYNTHETIC"}],
        "ancestry_disjointness_receipt": {"status": "PASS_SYNTHETIC"},
        "unresolved_noncomparable_manifest": {"ref": "synthetic-none"},
        "source_native_ancestry_ref": {"ref": "synthetic-ancestry"},
        "loss_profile": {"ref": "synthetic-loss-profile"},
        "holdout_generation_inputs_hash": "b" * 64,
        "canonicalization_spec": copy.deepcopy(harness.CANON),
        "manifest_hash": "",
    }
    manifest["manifest_hash"] = m.recompute_common_manifest_hash(manifest)
    return manifest


def _payload():
    units = [
        ("u1", "a", "x", "1", "1", "1"),
        ("u2", "a", "x", "1", "1", "1"),
        ("u3", "a", "x", "1", "1", "1"),
        ("u4", "a", "x", "2", "1", "1"),
        ("u5", "a", "z", "2", "2", "1"),
        ("u6", "b", "y", "2", "2", "2"),
    ]
    frozen_units = []
    for uid, p1, p2, d1, d2, d3 in units:
        frozen_units.append({
            "unit_id": uid,
            "exposed_measurement_ids": ["P1", "P2", "D1", "D2", "D3"],
            "position_states": {"P1": p1, "P2": p2},
            "disposition_states": {"D1": d1, "D2": d2, "D3": d3},
        })
    return {
        "schema_version": m.INPUT_SCHEMA_VERSION,
        "arm_id": "A",
        "common_semantic_input_manifest": _manifest(),
        "method_contract": {
            "position_measurement_ids": ["P1", "P2"],
            "disposition_measurement_ids": ["D1", "D2", "D3"],
            "minimum_exact_support": 2,
            "minimum_backoff_support": 2,
            "support_basis": "UNWEIGHTED_COUNT",
            "distribution_basis": "UNWEIGHTED_COUNT",
            "weighting_mode": "NONE",
            "backoff_mode": "DECLARED_NESTED_SUBSET_ONLY",
            "pruning_mode": "NONE",
        },
        "frozen_units": frozen_units,
        "query_manifest": [
            {
                "query_id": "Q_EXACT",
                "position_condition": {"P1": "a", "P2": "x"},
                "disposition_measurement_ids": ["D1", "D2", "D3"],
                "backoff_sequence": [["P1"]],
            },
            {
                "query_id": "Q_BACKOFF",
                "position_condition": {"P1": "b", "P2": "y"},
                "disposition_measurement_ids": ["D1", "D2", "D3"],
                "backoff_sequence": [["P1"], []],
            },
        ],
        "replay_context": {
            "code_version_ref": "SYNTHETIC-CODE-R1",
            "partition_manifest_ref": "SYNTHETIC-PARTITION",
            "partition_manifest_hash": "partition-hash",
            "query_manifest_ref": "SYNTHETIC-QUERY-MANIFEST",
            "hostile_fixture_refs": [],
            "execution_contract_ref": "FFX002-R2",
        },
    }


def test_same_unit_exact_config_and_higher_order_destination():
    result = m.produce_exact_configuration_set(_payload())
    config = result["configuration_set"]
    assert config["full_cross_surface_coexposed_unit_count"] == 6
    assert all(row["configuration_order"] == 3 for row in config["disposition_configuration_index"])
    shared = [
        row for row in result["configuration_to_disposition"]
        if {p["state_id"] for p in row["position_state_pairs"]} == {"a", "x"}
    ][0]
    assert shared["eligible_joint_support_n_unweighted"] == 4


def test_minority_alternative_and_exact_counterpattern_are_retained():
    result = m.produce_exact_configuration_set(_payload())
    row = [
        row for row in result["configuration_to_disposition"]
        if [(p["measurement_id"], p["state_id"]) for p in row["position_state_pairs"]]
        == [("P1", "a"), ("P2", "x")]
    ][0]
    assert row["counterpattern_status"] == "MULTIPLE_EXACT_DESTINATIONS_PRESENT"
    assert len(row["disposition_distribution"]) == 2
    counter = result["counterpattern_index"]
    assert len(counter) == 1
    assert counter[0]["position_configuration_id"] == row["position_configuration_id"]
    minority = [b for b in row["disposition_distribution"] if b["branch_status"] == "MINORITY_ALTERNATIVE"]
    assert len(minority) == 1
    assert minority[0]["support_n_unweighted"] == 1
    assert minority[0]["probability_unweighted"] == 0.25


def test_exact_query_answers_without_backoff():
    result = m.produce_exact_configuration_set(_payload())
    q = result["query_results"][0]
    assert q["query_status"] == "ANSWER_EXACT"
    assert q["information_relaxation"] == []
    assert q["selected_attempt"]["support_n_unweighted"] == 4
    assert len(q["selected_attempt"]["disposition_distribution"]) == 2


def test_sparse_query_uses_only_declared_nested_subset_backoff():
    result = m.produce_exact_configuration_set(_payload())
    q = result["query_results"][1]
    assert q["query_status"] == "ANSWER_DECLARED_BACKOFF"
    assert [a["support_n_unweighted"] for a in q["attempts"]] == [1, 1, 6]
    assert q["information_relaxation"] == ["P1", "P2"]
    assert q["distance_metric_used"] is False
    assert q["semantic_state_changed"] is False
    assert result["loss_manifest"]["runtime_query_relaxations"] == [{
        "query_id": "Q_BACKOFF",
        "loss_type": "DECLARED_QUERY_CONDITION_RELAXATION",
        "relaxed_position_measurement_ids": ["P1", "P2"],
        "raw_exact_attempt_retained": True,
        "semantic_state_changed": False,
    }]


def test_manifest_tamper_fails_closed():
    payload = _payload()
    payload["common_semantic_input_manifest"]["claim_scope_ref"] = "TAMPERED"
    with pytest.raises(m.CoreAContractError) as exc:
        m.produce_exact_configuration_set(payload)
    assert exc.value.status == "COMMON_INPUT_ARM_HASH_DIVERGENCE"


def test_exposure_is_never_inferred_from_state_or_missingness():
    payload = _payload()
    payload["frozen_units"][0]["exposed_measurement_ids"].remove("D3")
    with pytest.raises(m.CoreAContractError) as exc:
        m.produce_exact_configuration_set(payload)
    assert exc.value.status == "CORE_A_EXPOSURE_STATE_DIVERGENCE"


def test_undeclared_method_or_similarity_surface_is_rejected():
    payload = _payload()
    payload["method_contract"]["distance_metric"] = "hamming"
    with pytest.raises(m.CoreAContractError) as exc:
        m.produce_exact_configuration_set(payload)
    assert exc.value.status == "CORE_A_INPUT_SCHEMA_REJECTED"


def test_output_is_deterministic_and_replay_receipt_has_no_nondeterminism():
    first = m.produce_exact_configuration_set(_payload())
    second = m.produce_exact_configuration_set(copy.deepcopy(_payload()))
    assert m._json_bytes(first) == m._json_bytes(second)
    replay = first["replay_receipt"]
    assert replay["replay_status"] == "DETERMINISTIC_REPLAY_READY"
    assert replay["nondeterministic_operation_inventory"] == []
    assert replay["seed_usage"] == "NONE"
    assert replay["output_hashes"]["loss_manifest"] == m.stable_hash(first["loss_manifest"])


def test_manifest_set_arrays_canonicalize_independent_of_set_order():
    a = _manifest()
    b = copy.deepcopy(a)
    b["source_native_measurement_refs"] = list(reversed(b["source_native_measurement_refs"]))
    assert m.recompute_common_manifest_hash(b) == a["manifest_hash"]
    assert m.attest_common_manifest(b)["attestation_status"] == "ATTESTED_EQUAL"


def test_backoff_must_be_nested_and_cannot_change_states():
    payload = _payload()
    payload["query_manifest"][1]["backoff_sequence"] = [["P1"], ["P2"]]
    with pytest.raises(m.CoreAContractError) as exc:
        m.produce_exact_configuration_set(payload)
    assert exc.value.status == "CORE_A_QUERY_MANIFEST_INVALID"


def test_cli_writes_complete_deterministic_artifact_set(tmp_path: Path):
    payload = _payload()
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps(payload, sort_keys=True), encoding="utf-8")
    out1, out2 = tmp_path / "out1", tmp_path / "out2"
    assert cli_main(["--input", str(input_path), "--output-dir", str(out1)]) == 0
    assert cli_main(["--input", str(input_path), "--output-dir", str(out2)]) == 0
    assert sorted(p.name for p in out1.iterdir()) == sorted(m.OUTPUT_FILENAMES.values())
    for filename in m.OUTPUT_FILENAMES.values():
        assert (out1 / filename).read_bytes() == (out2 / filename).read_bytes()


def test_weighted_estimand_uses_only_frozen_analysis_weight():
    payload = _payload()
    payload["method_contract"]["distribution_basis"] = "ANALYSIS_WEIGHT"
    payload["method_contract"]["weighting_mode"] = "FROZEN_ANALYSIS_WEIGHT"
    for unit in payload["frozen_units"]:
        unit["analysis_weight"] = 1.0
    payload["frozen_units"][3]["analysis_weight"] = 10.0
    result = m.produce_exact_configuration_set(payload)
    row = [
        row for row in result["configuration_to_disposition"]
        if [(p["measurement_id"], p["state_id"]) for p in row["position_state_pairs"]]
        == [("P1", "a"), ("P2", "x")]
    ][0]
    weighted_modal = [b for b in row["disposition_distribution"] if b["branch_status"] == "MODAL"]
    assert len(weighted_modal) == 1
    assert weighted_modal[0]["support_n_unweighted"] == 1
    assert weighted_modal[0]["support_mass_analysis_weight"] == 10.0
    assert result["method_manifest"]["distribution_basis"] == "ANALYSIS_WEIGHT"


def test_weighted_query_abstains_when_bound_estimand_mass_is_zero():
    payload = _payload()
    payload["method_contract"]["distribution_basis"] = "ANALYSIS_WEIGHT"
    payload["method_contract"]["weighting_mode"] = "FROZEN_ANALYSIS_WEIGHT"
    for unit in payload["frozen_units"]:
        unit["analysis_weight"] = 0.0
    result = m.produce_exact_configuration_set(payload)
    assert result["query_results"][0]["query_status"] == "ABSTAIN_ZERO_ANALYSIS_WEIGHT_MASS"
