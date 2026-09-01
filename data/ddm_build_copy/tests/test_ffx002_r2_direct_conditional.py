from __future__ import annotations

import copy
import random

import pytest

from data.ddm_build_copy.ddm_ffx002_r2_direct_conditional import (
    DirectConditionalContractError,
    produce_direct_conditional_redistribution,
    recompute_common_manifest_hash,
)


def manifest():
    m = {
        "manifest_schema_version": "TEST_COMMON_R1",
        "current_execution_sha": "synthetic-sha",
        "observation_substrate_ref": {"ref": "synthetic-observations", "hash": "obs"},
        "respondent_entity_binding_ref": {"ref": "synthetic-respondents"},
        "exposure_risk_set_ref": {"ref": "synthetic-risk"},
        "source_scope_ref": {"source": "SYNTHETIC"},
        "source_native_measurement_refs": ["C1", "C2", "D1"],
        "qimpl_measurement_binding_refs": {"C1": "C1", "C2": "C2", "D1": "D1"},
        "response_state_semantics_ref": {"ref": "synthetic-response-semantics"},
        "special_state_semantics_ref": {"ref": "synthetic-special-states"},
        "ttar_execution_sequence": [],
        "post_transform_state_manifest": {"ref": "synthetic-frozen-states"},
        "claim_scope_ref": {"claim": "synthetic-P(D|C)"},
        "estimand_ref": {"estimand": "sample-descriptive"},
        "weight_design_refs": "NONE",
        "analytic_role_authority_refs": {"pra": "synthetic-pra"},
        "ancestry_disjointness_receipt": {"status": "PASS"},
        "unresolved_noncomparable_manifest": [],
        "source_native_ancestry_ref": {"ref": "synthetic-ancestry"},
        "loss_profile": [],
        "holdout_generation_inputs_hash": "synthetic-holdout-inputs",
        "canonicalization_spec": {
            "encoding": "UTF-8",
            "hash_algorithm": "sha256",
            "set_valued_paths": [],
        },
        "manifest_hash": "pending",
    }
    m["manifest_hash"] = recompute_common_manifest_hash(m)
    return m


def bundle():
    m = manifest()
    rows = []
    values = {
        "r1": ("c1", "x1", "d0"),
        "r2": ("c1", "x1", "d1"),
        "r3": ("c1", "x1", "d1"),
        "r4": ("c1", "x0", "d2"),
        "r5": ("c0", "x1", "d0"),
        "r6": ("c0", "x0", "d2"),
    }
    for rid, (c1, c2, d1) in values.items():
        for mid, sid in (("C1", c1), ("C2", c2), ("D1", d1)):
            rows.append(
                {
                    "respondent_id": rid,
                    "measurement_id": mid,
                    "state_id": sid,
                    "exposed": True,
                }
            )
    return {
        "common_manifest": m,
        "frozen_state_registry": {
            "post_transform_state_manifest_ref": m["post_transform_state_manifest"],
            "states_by_measurement": {
                "C1": ["c0", "c1"],
                "C2": ["x0", "x1"],
                "D1": ["d0", "d1", "d2"],
            },
        },
        "risk_set": {
            "risk_set_ref": m["exposure_risk_set_ref"],
            "respondent_ids": list(values),
        },
        "respondent_measurements": rows,
        "condition": {
            "condition_id": "C1=c1&C2=x1",
            "states": [
                {"measurement_id": "C1", "state_id": "c1"},
                {"measurement_id": "C2", "state_id": "x1"},
            ],
        },
        "outcome": {
            "outcome_id": "D1",
            "measurement_id": "D1",
            "destination_state_ids": ["d0", "d1", "d2"],
        },
        "support_policy": {
            "minimum_unweighted_support": 3,
            "minimum_effective_sample_size": None,
            "backoff_steps": [],
            "allow_unconditional_backoff": False,
        },
        "estimand_design": {
            "estimand_ref": m["estimand_ref"],
            "weight_design_refs": m["weight_design_refs"],
            "weight_by_respondent": None,
            "uncertainty": {
                "method": "KISH_WILSON_SCORE_R1",
                "confidence_level": 0.95,
            },
        },
        "analytic_role_binding_ref": m["analytic_role_authority_refs"],
    }


def run(b):
    return produce_direct_conditional_redistribution(**b)


def errcode(b):
    with pytest.raises(DirectConditionalContractError) as exc:
        run(b)
    return exc.value.code


def probs(result):
    return [row["probability"] for row in result["destination_distribution"]]


def test_exact_distribution_retains_full_destination_and_minority_states():
    result = run(bundle())
    assert result["status"] == "ESTIMATED__EXACT_CONDITION"
    assert [x["destination_state_id"] for x in result["destination_distribution"]] == ["d0", "d1", "d2"]
    assert probs(result) == [0.333333333333, 0.666666666667, 0.0]
    assert result["destination_distribution"][2]["unweighted_count"] == 0
    assert result["destination_distribution"][0]["ci_lower"] is not None
    assert result["common_manifest_attestation"]["attestation_status"] == "ATTESTED_EQUAL"
    assert result["loss_receipt"]["receipt_type"] == "TYPED_LOSS_RECEIPT"
    assert result["replay_receipt"]["receipt_type"] == "TYPED_REPLAY_RECEIPT"


def test_governed_weights_are_consumed_and_change_estimand_distribution():
    b = bundle()
    b["common_manifest"]["weight_design_refs"] = {"ref": "synthetic-weight-design"}
    b["common_manifest"]["manifest_hash"] = recompute_common_manifest_hash(b["common_manifest"])
    b["estimand_design"]["weight_design_refs"] = b["common_manifest"]["weight_design_refs"]
    b["estimand_design"]["weight_by_respondent"] = {
        rid: (8.0 if rid == "r1" else 1.0)
        for rid in b["risk_set"]["respondent_ids"]
    }
    result = run(b)
    assert probs(result) == [0.8, 0.2, 0.0]
    assert result["estimand_design"]["weight_mode"] == "GOVERNED_RESPONDENT_WEIGHTS_CONSUMED"


def test_exact_risk_set_noncoexposure_fails_closed():
    b = bundle()
    for row in b["respondent_measurements"]:
        if row["respondent_id"] == "r6" and row["measurement_id"] == "D1":
            row["exposed"] = False
    assert errcode(b) == "EXPERIMENT_INVALID__RESPONDENT_OR_EXPOSURE_AUTHORITY"


def test_missing_measurement_row_cannot_be_used_as_exposure_proxy():
    b = bundle()
    b["respondent_measurements"] = [
        row for row in b["respondent_measurements"]
        if not (row["respondent_id"] == "r6" and row["measurement_id"] == "D1")
    ]
    assert errcode(b) == "DIRECT_CONDITIONAL_COEXPOSURE_UNPROVED"


def test_preregistered_backoff_only_relaxes_exact_predicates_and_is_typed():
    b = bundle()
    b["support_policy"] = {
        "minimum_unweighted_support": 4,
        "minimum_effective_sample_size": None,
        "backoff_steps": [
            {
                "backoff_id": "DROP_C2",
                "states": [{"measurement_id": "C1", "state_id": "c1"}],
            }
        ],
        "allow_unconditional_backoff": False,
    }
    result = run(b)
    assert result["status"] == "ESTIMATED__BACKOFF_USED"
    assert result["support_policy"]["selected_condition"]["selection_id"] == "DROP_C2"
    assert result["support_policy"]["selected_condition"]["relaxed_exact_states"] == [
        {"measurement_id": "C2", "state_id": "x1"}
    ]
    assert any(x["loss_code"] == "CONDITION_SPECIFICITY_RELAXED" for x in result["loss_receipt"]["losses"])
    assert probs(result) == [0.25, 0.5, 0.25]


def test_insufficient_support_abstains_but_keeps_all_destination_states_and_counts():
    b = bundle()
    b["support_policy"]["minimum_unweighted_support"] = 5
    result = run(b)
    assert result["status"] == "ABSTAINED__INSUFFICIENT_SUPPORT"
    assert probs(result) == [None, None, None]
    assert [x["unweighted_count"] for x in result["destination_distribution"]] == [1, 2, 0]


def test_manifest_tamper_is_postfork_semantic_divergence():
    b = bundle()
    b["common_manifest"]["claim_scope_ref"] = {"claim": "tampered-after-hash"}
    assert errcode(b) == "EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE"


def test_outcome_state_pooling_or_omission_is_forbidden():
    b = bundle()
    b["outcome"]["destination_state_ids"] = ["d0", "d1"]
    assert errcode(b) == "DIRECT_CONDITIONAL_OUTCOME_STATE_POOLING_FORBIDDEN"


def test_backoff_cannot_replace_rebin_or_reorder_semantic_state():
    b = bundle()
    b["support_policy"] = {
        "minimum_unweighted_support": 4,
        "minimum_effective_sample_size": None,
        "backoff_steps": [
            {
                "backoff_id": "ILLEGAL_REPLACEMENT",
                "states": [{"measurement_id": "C1", "state_id": "c0"}],
            }
        ],
        "allow_unconditional_backoff": False,
    }
    assert errcode(b) == "DIRECT_CONDITIONAL_BACKOFF_SEMANTIC_CHANGE_FORBIDDEN"


def test_estimand_switch_fails_closed():
    b = bundle()
    b["estimand_design"]["estimand_ref"] = {"estimand": "different"}
    assert errcode(b) == "EXPERIMENT_INVALID__ESTIMAND_DIVERGENCE"


def test_numeric_replay_is_invariant_to_respondent_input_row_order():
    b1 = bundle()
    b2 = copy.deepcopy(b1)
    random.Random(7331).shuffle(b2["respondent_measurements"])
    r1 = run(b1)
    r2 = run(b2)
    assert r1["output_hash"] == r2["output_hash"]
    assert r1["replay_receipt"]["input_hashes"] == r2["replay_receipt"]["input_hashes"]
    assert r1["destination_distribution"] == r2["destination_distribution"]


def test_output_explicitly_refuses_v551_relabeling():
    result = run(bundle())
    assert result["semantic_non_equivalence_notice"].startswith("NOT_V551_CONDITIONAL_DETERMINICITY")


def test_unknown_observed_state_is_rejected_not_rebinned():
    b = bundle()
    b["respondent_measurements"][0]["state_id"] = "invented-state"
    assert errcode(b) == "DIRECT_CONDITIONAL_UNKNOWN_FROZEN_STATE"


def test_postfork_role_binding_change_is_rejected():
    b = bundle()
    b["analytic_role_binding_ref"] = {"pra": "different"}
    assert errcode(b) == "DIRECT_CONDITIONAL_ANALYTIC_ROLE_DIVERGENCE"
