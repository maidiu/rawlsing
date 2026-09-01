from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from data.ddm_build_copy import field_forge_ffx002_harness as harness
from data.ddm_build_copy import ffx002_r2_integrated_stack as stack


STATE_CATALOG = {
    "P1": ["a", "b"],
    "P2": ["x", "y"],
    "D1": ["d0", "d1", "d2"],
    "D2": ["e0", "e1"],
    "D3": ["f0", "f1"],
}


def _common_and_holdout():
    all_ids = [f"r{i:02d}" for i in range(1, 15)]
    selected = None
    for i in range(100):
        inp = harness.holdout_inputs(all_ids, f"integrated-seed-{i}", 2000, "synthetic-stack@1", {"numeric": "synthetic"})
        source = {
            "manifest_schema_version": harness.SCHEMA_VERSION,
            "current_execution_sha": "a" * 40,
            "observation_substrate_ref": {"ref": "synthetic://observations"},
            "respondent_entity_binding_ref": {"ref": "synthetic://respondents"},
            "exposure_risk_set_ref": {"ref": "synthetic://risk-set"},
            "source_scope_ref": {"ref": "synthetic://scope"},
            "source_native_measurement_refs": [{"id": x} for x in STATE_CATALOG],
            "qimpl_measurement_binding_refs": [{"id": f"Q:{x}"} for x in STATE_CATALOG],
            "response_state_semantics_ref": {"ref": "synthetic://response"},
            "special_state_semantics_ref": {"ref": "synthetic://special"},
            "ttar_execution_sequence": "NONE",
            "post_transform_state_manifest": {"ref": "synthetic://frozen-states"},
            "claim_scope_ref": {"ref": "synthetic://claim"},
            "estimand_ref": {"ref": "synthetic://sample-descriptive"},
            "weight_design_refs": "NONE",
            "analytic_role_authority_refs": [{"id": "PRA:SYNTHETIC"}],
            "ancestry_disjointness_receipt": {"ref": "synthetic://ancestry-pass"},
            "unresolved_noncomparable_manifest": {"ref": "synthetic://none"},
            "source_native_ancestry_ref": {"ref": "synthetic://source-ancestry"},
            "loss_profile": {"ref": "synthetic://loss-none"},
            "holdout_generation_inputs_hash": harness.hash_payload(inp),
            "canonicalization_spec": copy.deepcopy(harness.CANON),
        }
        common = harness.compile_common_manifest(source)
        holdout = harness.freeze_holdout(common, inp)
        if len(holdout["design_unit_ids"]) >= 8 and len(holdout["final_holdout_unit_ids"]) >= 1:
            selected = common, holdout
            break
    assert selected is not None
    return selected


def _values(design_ids):
    patterns = [
        ("a", "x", "d0", "e0", "f0"),
        ("a", "x", "d1", "e0", "f0"),
        ("a", "x", "d1", "e1", "f0"),
        ("a", "x", "d2", "e1", "f1"),
        ("a", "y", "d2", "e0", "f1"),
        ("b", "x", "d0", "e1", "f0"),
        ("b", "y", "d1", "e0", "f1"),
        ("b", "y", "d2", "e1", "f1"),
    ]
    out = {}
    for i, rid in enumerate(design_ids):
        out[rid] = patterns[i % len(patterns)]
    return out


def _b_method():
    return {
        "schema_version": "FFX002_R2_LOCAL_GEOMETRIC_METHOD_R1",
        "metric": {"family": "EXACT_STATE_HAMMING_R1", "state_comparison": "EXACT_FROZEN_STATE_IDENTITY_ONLY"},
        "decomposition": {"family": "CLASSICAL_MDS_JACOBI_R1", "axis_labels": "NUMERIC_IDS_ONLY"},
        "dimensionality": {"rule": "FIXED_R1", "retained_d": 2},
        "neighborhood": {"k": 2},
        "compression": {"float_digits": 12},
        "preprocessing": [{
            "name": "opaque_state_identity_projection",
            "classification": "IDENTITY_PRESERVING_METHOD",
            "executed_postfork": True,
        }],
    }


def _surface(side, mids, role, design_ids, values):
    index = {"P1": 0, "P2": 1, "D1": 2, "D2": 3, "D3": 4}
    return {
        "side": side,
        "measurements": [
            {
                "measurement_id": mid,
                "analytic_role": role,
                "state_ids": list(STATE_CATALOG[mid]),
                "ancestry_ids": [f"ANCESTRY:{side}:{mid}"],
                "component_id": "C0",
            }
            for mid in mids
        ],
        "rows": [
            {
                "respondent_id": rid,
                "state_by_measurement": {mid: values[rid][index[mid]] for mid in mids},
            }
            for rid in design_ids
        ],
    }


def _bundle():
    common, holdout = _common_and_holdout()
    design_ids = holdout["design_unit_ids"]
    values = _values(design_ids)

    a_queries = [{
        "query_id": "A_Q1",
        "position_condition": {"P1": "a", "P2": "x"},
        "disposition_measurement_ids": ["D1"],
        "backoff_sequence": [["P1"]],
    }]
    query_rows = [
        {
            "query_id": "Q01",
            "views_permitted": ["A", "B", "C"],
            "arm_query_refs": {"A": "A_Q1", "C": "C_Q1"},
            "abstention_rule": "ABSTAIN_IF_NO_LAWFUL_ADAPTER",
        },
        {
            "query_id": "Q05",
            "views_permitted": ["B"],
            "arm_query_refs": {"B": "POSITION_LOCAL_NEIGHBORHOOD"},
            "abstention_rule": "DOES_NOT_REPRESENT_FOR_A_OR_C",
        },
        {
            "query_id": "Q_UNSUPPORTED",
            "views_permitted": [],
            "arm_query_refs": {},
            "abstention_rule": "DOES_NOT_REPRESENT",
        },
    ]
    queries = harness.freeze_queries(common, holdout, query_rows)

    units = []
    rows = []
    for rid in design_ids:
        p1, p2, d1, d2, d3 = values[rid]
        state_by = {"P1": p1, "P2": p2, "D1": d1, "D2": d2, "D3": d3}
        units.append({
            "unit_id": rid,
            "exposed_measurement_ids": list(STATE_CATALOG),
            "position_states": {"P1": p1, "P2": p2},
            "disposition_states": {"D1": d1, "D2": d2, "D3": d3},
        })
        for mid, sid in state_by.items():
            rows.append({"respondent_id": rid, "measurement_id": mid, "state_id": sid, "exposed": True})

    arm_a = {
        "schema_version": "FFX_EXACT_CONFIGURATION_INPUT_R1",
        "arm_id": "A",
        "method_contract": {
            "position_measurement_ids": ["P1", "P2"],
            "disposition_measurement_ids": ["D1", "D2", "D3"],
            "minimum_exact_support": 1,
            "minimum_backoff_support": 1,
            "support_basis": "UNWEIGHTED_COUNT",
            "distribution_basis": "UNWEIGHTED_COUNT",
            "weighting_mode": "NONE",
            "backoff_mode": "DECLARED_NESTED_SUBSET_ONLY",
            "pruning_mode": "NONE",
        },
        "frozen_units": units,
        "query_manifest": a_queries,
        "replay_context": {
            "code_version_ref": "A:SYNTHETIC@1",
            "partition_manifest_ref": "HOLDOUT:SYNTHETIC@1",
            "partition_manifest_hash": holdout["holdout_manifest_hash"],
            "query_manifest_ref": "QUERY:SYNTHETIC@1",
            "hostile_fixture_refs": [],
            "execution_contract_ref": stack.DESIGN_REF,
        },
        "common_semantic_input_manifest": copy.deepcopy(common),
    }
    arm_b = {
        "method_manifest": _b_method(),
        "position_surface": _surface("position", ["P1", "P2"], "ACTIVE_POSITION", design_ids, values),
        "disposition_surface": _surface("disposition", ["D1", "D2", "D3"], "ACTIVE_DISPOSITION", design_ids, values),
        "common_manifest": copy.deepcopy(common),
    }
    arm_c = {
        "frozen_state_registry": {
            "post_transform_state_manifest_ref": common["post_transform_state_manifest"],
            "states_by_measurement": copy.deepcopy(STATE_CATALOG),
        },
        "risk_set": {
            "risk_set_ref": common["exposure_risk_set_ref"],
            "respondent_ids": list(design_ids),
        },
        "respondent_measurements": rows,
        "estimand_design": {
            "estimand_ref": common["estimand_ref"],
            "weight_design_refs": common["weight_design_refs"],
            "weight_by_respondent": None,
            "uncertainty": {"method": "KISH_WILSON_SCORE_R1", "confidence_level": 0.95},
        },
        "analytic_role_binding_ref": copy.deepcopy(common["analytic_role_authority_refs"]),
        "requests": [{
            "query_id": "C_Q1",
            "condition": {
                "condition_id": "P1=a&P2=x",
                "states": [
                    {"measurement_id": "P1", "state_id": "a"},
                    {"measurement_id": "P2", "state_id": "x"},
                ],
            },
            "outcome": {
                "outcome_id": "D1",
                "measurement_id": "D1",
                "destination_state_ids": ["d0", "d1", "d2"],
            },
            "support_policy": {
                "minimum_unweighted_support": 1,
                "minimum_effective_sample_size": None,
                "backoff_steps": [],
                "allow_unconditional_backoff": False,
            },
        }],
        "common_manifest": copy.deepcopy(common),
    }

    return {
        "schema_version": stack.INPUT_SCHEMA_VERSION,
        "common_manifest": common,
        "holdout_manifest": holdout,
        "query_manifest": queries,
        "execution_code_refs": {
            "stack": "FFP013:SYNTHETIC@1",
            "A": "862279e95100bc1c57acb0ead0695eb8c27cbcd7:data/ddm_build_copy/ddm_ffx_exact_configuration.py",
            "B": "db912242e0f6bfefa61a2a83e11f701d17947af4:data/ddm_build_copy/ffx002_r2_local_geometry.py",
            "C": "38bc815d3edc8d8c75c8d8240de1da24cc588e5b:data/ddm_build_copy/ddm_ffx002_r2_direct_conditional.py",
        },
        "arm_inputs": {"A": arm_a, "B": arm_b, "C": arm_c},
        "hostile_rows": [
            {
                "perturbation_id": "R2F001",
                "views_attacked": "ALL",
                "semantic_input_handling": "ILLEGAL_POSTFORK",
                "failure_state": "EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE",
            },
            {
                "perturbation_id": "R2F004",
                "views_attacked": "ALL",
                "semantic_input_handling": "NEW_COMMON_INPUT_VARIANT",
                "failure_state": "VIEW_SENSITIVE__BLOCK_DEPENDENCE",
            },
        ],
        "citc": {
            "citc_ref": "CITC:SYNTHETIC_EXTERNAL@1",
            "rules": [
                {"metric_id": "QUERY_COVERAGE", "operator": "GE", "threshold": 1.0},
                {"metric_id": "TV_DISTANCE", "operator": "LE", "threshold": 1.0},
                {"metric_id": "LOG_LOSS", "operator": "LE", "threshold": 100.0},
            ],
        },
        "scoring_cases": [{
            "query_id": "Q01",
            "truth_distribution": [
                {"state_id": "d0", "probability": 0.25},
                {"state_id": "d1", "probability": 0.50},
                {"state_id": "d2", "probability": 0.25},
            ],
        }],
    }


def _bomb(*args, **kwargs):
    raise AssertionError("producer executed after a preflight-invalid bundle")


def test_integrated_stack_all_three_arms_attest_identical_common_hash():
    b = _bundle()
    result = stack.run_integrated_stack(b)
    att = result["common_hash_attestation"]
    assert att["status"] == "A_B_C_ATTEST_IDENTICAL"
    assert set(att["arm_recomputed_hashes"].values()) == {b["common_manifest"]["manifest_hash"]}
    assert result["terminal_state"] == stack.TERMINAL_READY


def test_one_arm_semantic_tamper_fails_before_any_producer_execution(monkeypatch):
    b = _bundle()
    tampered = copy.deepcopy(b["common_manifest"])
    tampered["estimand_ref"] = {"ref": "synthetic://different-estimand"}
    tampered["manifest_hash"] = harness.compute_common_hash(tampered)
    b["arm_inputs"]["B"]["common_manifest"] = tampered
    monkeypatch.setattr(stack.core_a, "produce_exact_configuration_set", _bomb)
    monkeypatch.setattr(stack.core_b, "compile_local_geometric_view", _bomb)
    monkeypatch.setattr(stack.core_c, "produce_direct_conditional_redistribution", _bomb)
    with pytest.raises(stack.IntegratedStackError) as exc:
        stack.run_integrated_stack(b)
    assert exc.value.state == "FORK_SEMANTIC_TAMPER__COMMON_MANIFEST_HASH_DIVERGENCE"


def test_risk_set_divergence_fails_preflight():
    b = _bundle()
    b["arm_inputs"]["C"]["risk_set"]["respondent_ids"].pop()
    with pytest.raises(stack.IntegratedStackError) as exc:
        stack.preflight_integrated_bundle(b)
    assert exc.value.state == "COMMON_INPUT_RISK_SET_DIVERGENCE"


def test_estimand_divergence_fails_preflight():
    b = _bundle()
    b["arm_inputs"]["C"]["estimand_design"]["estimand_ref"] = {"ref": "other"}
    with pytest.raises(stack.IntegratedStackError) as exc:
        stack.preflight_integrated_bundle(b)
    assert exc.value.state == "COMMON_INPUT_ESTIMAND_DIVERGENCE"


@pytest.mark.parametrize("forbidden_key", ["state_merge_rule", "rebin_rule", "role_override"])
def test_postfork_state_merge_rebin_rerole_fails(forbidden_key):
    b = _bundle()
    b["arm_inputs"]["B"]["method_manifest"][forbidden_key] = "forbidden"
    with pytest.raises(stack.IntegratedStackError) as exc:
        stack.preflight_integrated_bundle(b)
    assert exc.value.state == "EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE"


def test_no_arm_can_consume_another_arms_learned_output():
    b = _bundle()
    b["arm_inputs"]["C"]["learned_outputs"] = {"A": {"fake": True}}
    with pytest.raises(stack.IntegratedStackError) as exc:
        stack.preflight_integrated_bundle(b)
    assert exc.value.state == "EXPERIMENT_INVALID__CROSS_ARM_LEARNED_OUTPUT_CONSUMPTION"


def test_minority_destination_states_remain_represented_in_a_and_c():
    result = stack.run_integrated_stack(_bundle())
    a_q = result["arm_outputs"]["A"]["query_results"][0]
    a_states = {
        row["state_pairs"][0]["state_id"]
        for row in a_q["selected_attempt"]["disposition_distribution"]
    }
    c_states = {
        row["destination_state_id"]
        for row in result["arm_outputs"]["C"][0]["result"]["destination_distribution"]
    }
    assert {"d0", "d1", "d2"} <= a_states
    assert c_states == {"d0", "d1", "d2"}
    assert any(
        row["branch_status"] == "MINORITY_ALTERNATIVE"
        for row in a_q["selected_attempt"]["disposition_distribution"]
    )


def test_unsupported_queries_abstain_or_do_not_represent_instead_of_translating():
    result = stack.run_integrated_stack(_bundle())
    rows = result["query_results"]["results"]
    unsupported = [r for r in rows if r["query_id"] == "Q_UNSUPPORTED"]
    assert {r["query_status"] for r in unsupported} == {"DOES_NOT_REPRESENT"}
    b_q01 = next(r for r in rows if r["query_id"] == "Q01" and r["arm_id"] == "B")
    assert b_q01["query_status"] == "ABSTAIN__NO_DECLARED_ARM_QUERY_ADAPTER"
    assert b_q01["answer"] is None


def test_replay_receipts_bind_exact_code_input_and_output_identities():
    b = _bundle()
    result = stack.run_integrated_stack(b)
    receipts = result["receipt_collection"]
    assert receipts["common_manifest_hash"] == b["common_manifest"]["manifest_hash"]
    assert receipts["holdout_manifest_hash"] == b["holdout_manifest"]["holdout_manifest_hash"]
    assert receipts["query_manifest_hash"] == b["query_manifest"]["query_manifest_hash"]
    for arm in harness.CORE:
        row = receipts["arm_receipts"][arm]
        assert row["code_identity_ref"] == b["execution_code_refs"][arm]
        assert row["arm_input_hash"] == stack._hash(b["arm_inputs"][arm])
        assert row["arm_output_hash"] == stack._hash(result["arm_outputs"][arm])
        assert row["common_manifest_hash"] == b["common_manifest"]["manifest_hash"]


def test_fork_semantic_tamper_hostile_rejects_a_b_c():
    result = stack.run_integrated_stack(_bundle())
    receipt = result["fork_semantic_tamper_receipt"]
    assert receipt["hostile_id"] == "FORK_SEMANTIC_TAMPER__COMMON_MANIFEST_HASH_DIVERGENCE"
    assert {row["arm_id"] for row in receipt["cases"]} == {"A", "B", "C"}
    assert {row["status"] for row in receipt["cases"]} == {"PASS__REJECTED_BEFORE_EXECUTION"}


def test_citc_thresholds_are_consumed_not_hardcoded_and_never_select_view():
    obs = [{"query_id": "Q", "arm_id": "A", "metric_id": "TV_DISTANCE", "value": 0.4, "status": "MEASURED"}]
    loose = {"citc_ref": "CITC:1", "rules": [{"metric_id": "TV_DISTANCE", "operator": "LE", "threshold": 0.5}]}
    strict = {"citc_ref": "CITC:2", "rules": [{"metric_id": "TV_DISTANCE", "operator": "LE", "threshold": 0.3}]}
    assert stack.apply_citc(obs, loose)["rulings"][0]["materiality_rule_result"] is True
    assert stack.apply_citc(obs, strict)["rulings"][0]["materiality_rule_result"] is False
    assert stack.apply_citc(obs, loose)["preferred_view"] is None
    assert stack.apply_citc(obs, loose)["master_score"] is None


def test_prev3_plumbing_contains_no_actor_interpretation():
    result = stack.run_integrated_stack(_bundle())
    prev3 = result["prev3_ablation"]
    assert set(p["packet_id"] for p in prev3["packets"]) == {"P0", "P1", "P2", "P3"}
    assert all(p["actor_interpretation"] == "PROHIBITED" for p in prev3["packets"])
    assert "PERSONALITY" in prev3["forbidden_outputs"]


def test_write_integrated_outputs_is_deterministic(tmp_path: Path):
    result = stack.run_integrated_stack(_bundle())
    a = tmp_path / "a"
    b = tmp_path / "b"
    h1 = stack.write_integrated_outputs(result, a)
    h2 = stack.write_integrated_outputs(result, b)
    assert h1 == h2
    assert sorted(p.name for p in a.iterdir()) == sorted(p.name for p in b.iterdir())
    for name in h1:
        assert (a / name).read_bytes() == (b / name).read_bytes()


def test_special_state_semantics_cannot_be_redefined_in_one_arm():
    b = _bundle()
    b["arm_inputs"]["A"]["special_state_semantics_ref"] = {"ref": "arm-local-special-state"}
    with pytest.raises(stack.IntegratedStackError) as exc:
        stack.preflight_integrated_bundle(b)
    assert exc.value.state == "EXPERIMENT_INVALID__POSTFORK_SPECIAL_STATE_DIVERGENCE"


def test_ablation_plan_explicitly_carries_weaker_added_removed_and_multiview_packages():
    result = stack.run_integrated_stack(_bundle())
    plan = result["ablation_plan"]
    assert [p["package_id"] for p in plan["packages"]] == ["SUBSTRATE", "C", "A+C", "B+C", "A+B", "A+B+C"]
    rows = {row["target_view"]: row for row in plan["target_add_remove_rows"]}
    assert rows["A"]["target_removed_package"] == "B+C"
    assert rows["B"]["target_removed_package"] == "A+C"
    assert rows["C"]["target_removed_package"] == "A+B"
    assert plan["preferred_view"] is None
    assert plan["master_score"] is None


def test_cli_entrypoint_runs_complete_synthetic_stack(tmp_path: Path):
    bundle_path = tmp_path / "bundle.json"
    output_dir = tmp_path / "out"
    bundle_path.write_text(json.dumps(_bundle(), sort_keys=True), encoding="utf-8")
    assert stack.main(["--input-json", str(bundle_path), "--output-dir", str(output_dir)]) == 0
    summary = json.loads((output_dir / "00_INTEGRATED_EXECUTION_RETURN.json").read_text(encoding="utf-8"))
    assert summary["terminal_state"] == stack.TERMINAL_READY
    assert (output_dir / "10_REPLAY_OUTPUT_RECEIPTS.json").is_file()
