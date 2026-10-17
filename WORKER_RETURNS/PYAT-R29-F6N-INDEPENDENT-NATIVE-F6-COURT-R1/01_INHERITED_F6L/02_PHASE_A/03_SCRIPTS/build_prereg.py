"""Build the F6L Phase-A preregistration JSON.

This script only constructs inputs and computes exact expectations with the
independent engine.  It never imports or executes the native producer.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RET / "01_STAGED_NATIVE"))
sys.path.insert(0, str(RET / "01_SOURCE_TRANSPORT/F6C_AUTHOR"))
sys.path.insert(0, str(RET / "02_PHASE_A/03_SCRIPTS"))

import f6l_expectations as E  # noqa: E402
import f6l_worlds as W  # noqa: E402
import f6c_worlds  # noqa: E402

OUT = RET / "02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json"


def expectations(world, min_raw_support=None):
    policy = world["policy"]
    support = (policy["minimum_raw_support"] if min_raw_support is None
               else min_raw_support)
    result = E.standardize(world["target"]["strata"],
                           W.tables_for_engine(world),
                           policy["source_weights"], support)
    sens = E.sensitivity(result["lower"], result["upper"],
                         (policy["mapping_bias_radius"],
                          policy["transport_bias_radius"],
                          policy["target_share_bias_radius"]))
    out = {
        "exact_joint_covered_subprobability": E.map_to_cells(result["joint"]),
        "exact_lower": E.map_to_cells(result["lower"]),
        "exact_upper": E.map_to_cells(result["upper"]),
        "exact_bias_sensitivity": {
            "radius": E.s(sens["radius"]),
            "lower": E.map_to_cells(sens["lower"]),
            "upper": E.map_to_cells(sens["upper"]),
        },
        "covered_subprobability_sum": E.s(sum(result["joint"].values(), E.F(0))),
        "uncovered_target_mass": E.s(result["uncovered"]),
        "distribution_is_complete": result["uncovered"] == 0,
        "coverage": result["coverage"],
        "keys_in_declared_order": [list(k) for k in
                                   __import__("itertools").product(
                                       *world["labels"])],
    }
    if result["uncovered"] == 0:
        cond = E.conditional(result["joint"], world["axes"],
                             {world["axes"][0]: "LOW"}, world["axes"][1])
        out["exact_conditional_yes_given_low"] = {
            "model_denominator_mass": E.s(cond["denominator"]),
            "probabilities": {k: E.s(v) for k, v in cond["probabilities"].items()},
        }
    return out


def main():
    p1 = W.original_f6c_world_b(f6c_worlds)
    p2 = W.novel_2x2_no_positivity()
    p3 = W.novel_3cat_no_positivity()
    p11 = W.positive_2x2()
    p10 = W.positive_2x2_substituted()
    p8_low = W.distributed_support(1)
    p8_cell = W.distributed_support(5)
    p8_exclude = W.distributed_support(150)

    worlds = []
    for world, extra in (
        (p1, {"case": "P1_ORIGINAL_UNCOVERED_WORLD"}),
        (p2, {"case": "P2_NOVEL_2X2_NO_POSITIVITY"}),
        (p3, {"case": "P3_NOVEL_3_CATEGORY_NO_POSITIVITY"}),
        (p11, {"case": "P11_GENUINE_COMPLETE_TARGET_POSITIVE"}),
        (p10, {"case": "P10_ARITHMETIC_SOURCE_SUBSTITUTION"}),
        (p8_low, {"case": "P8_DISTRIBUTED_SUPPORT_MIN_1"}),
        (p8_cell, {"case": "P8_DISTRIBUTED_SUPPORT_MIN_5_CELL_NOT_GATE"}),
        (p8_exclude, {"case": "P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED"}),
    ):
        entry = {**extra,
                 "world_id": world["world_id"],
                 "origin": world["origin"],
                 "target": world["target"],
                 "sources": world["sources"],
                 "policy": world["policy"],
                 "axes": world["axes"],
                 "labels": world["labels"],
                 "exact_expectations": expectations(world)}
        worlds.append(entry)

    cases = [
        {
            "id": "P1_ORIGINAL_UNCOVERED_WORLD",
            "world": "F6L_P1_ORIGINAL_F6C_WORLD_B_UNCOVERED",
            "question": "Does the original uncovered-mass world keep null distribution, 4/5 covered mass and widened upper bounds without issuing a complete-target decision?",
            "expected_good_conditional_result": {
                "distribution": None,
                "covered_subprobability": ["8/25", "2/25", "2/25", "8/25"],
                "covered_sum": "4/5",
                "uncovered_target_mass": "1/5",
                "upper": ["19/25", "7/25", "7/25", "19/25"],
                "lower": ["2/25", "2/25", "2/25", "2/25"],
                "consumer": "UNAVAILABLE/NO_COMPLETE_TARGET_JOINT",
            },
            "expected_safe_status": "decision must not assert a complete synthetic target joint; partial/no-complete typed status required; covered bounds must remain readable",
            "expected_actual_pre_repair": {
                "decision": "SYNTHETIC_CANDIDATE",
                "candidate_distribution": None,
                "uncovered_target_mass": "1/5",
                "consumer_state": "UNAVAILABLE",
                "consumer_reason": "NO_COMPLETE_TARGET_JOINT",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P2_NOVEL_2X2_NO_POSITIVITY",
            "world": "F6L_P2_NOVEL_2X2_UNCOVERED_THIRD",
            "question": "A novel 2x2 world whose second target stratum is covered by no source: are exact covered masses preserved and is a null distribution never served as a complete joint?",
            "expected_good_conditional_result": {
                "distribution": None,
                "covered_subprobability_sum": "2/3",
                "uncovered_target_mass": "1/3",
                "exact_joint_covered_subprobability": "3/20, 11/60, 11/60, 3/20",
                "exact_upper": "17/30, 3/5, 8/15, 1/2",
                "exact_lower": "1/15, 1/10, 1/6, 2/15",
            },
            "expected_safe_status": "no complete-target token; typed partial/no-complete status; conditional consumer UNAVAILABLE",
            "expected_actual_pre_repair": {
                "decision": "SYNTHETIC_CANDIDATE",
                "candidate_distribution": None,
                "uncovered_target_mass": "1/3",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P3_NOVEL_3_CATEGORY_NO_POSITIVITY",
            "world": "F6L_P3_NOVEL_3X2_UNCOVERED_QUARTER",
            "question": "A novel 3x2 world with a 1/4 uncovered target stratum: are six covered cells and bounds exact and is the decision partial?",
            "expected_good_conditional_result": {
                "distribution": None,
                "covered_subprobability_sum": "3/4",
                "uncovered_target_mass": "1/4",
                "exact_joint_covered_subprobability": "9/80, 9/80, 3/20, 3/16, 9/80, 3/40",
                "exact_upper": "2/5, 2/5, 19/40, 19/40, 2/5, 13/40",
                "exact_lower": "3/40, 3/40, 3/40, 3/20, 3/40, 3/40",
            },
            "expected_safe_status": "no complete-target token; typed partial/no-complete status; six covered bounds preserved",
            "expected_actual_pre_repair": {
                "decision": "SYNTHETIC_CANDIDATE",
                "candidate_distribution": None,
                "uncovered_target_mass": "1/4",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P4_FORGED_REAL_SOURCE_ADMIT_TRUE",
            "world": "F6L_P11_COMPLETE_POSITIVE",
            "question": "Can a caller-supplied admit=lambda True forge EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE for two real sources?",
            "expected_good_conditional_result": {
                "unchanged_arithmetic": "P11 exact joint remains available; arithmetic is not the contested object",
            },
            "expected_safe_status": "no EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE claim from an unverified boolean; either refuse or ceiling UNVERIFIED/TEST_ONLY; owner boundary remains UNVERIFIED",
            "expected_actual_pre_repair": {
                "admission_required": True,
                "callback_invocations": 4,
                "callback_identity_scope_operation_permission_checks": 0,
                "decision": "INFERRED_CANDIDATE_REQUIRES_REVIEW",
                "native_authority_ceiling": "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE",
                "mapped_authority_ceiling": "ABSENT",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P5_TEST_ORIGIN_BYPASS",
            "world": "F6L_P11_COMPLETE_POSITIVE",
            "question": "Does caller-declared test_origin=True bypass admission entirely and still let test-only nodes claim real-use authority?",
            "expected_good_conditional_result": {
                "arithmetic": "complete positive joint remains exact",
            },
            "expected_safe_status": "test-only output may remain complete synthetic test output, but no node may claim real-source authority; test flag is not authentication",
            "expected_actual_pre_repair": {
                "callback_invocations": 0,
                "decision": "SYNTHETIC_CANDIDATE",
                "test_origin": True,
                "native_authority_ceiling": "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE",
                "mapped_authority_ceiling": "ABSENT",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P5B_MIXED_ORIGIN_CONTAMINATION",
            "world": "F6L_P11_COMPLETE_POSITIVE",
            "question": "Can one caller-declared test source bypass admission while a genuinely real source is admitted, producing a real-looking output that contains unverified test data?",
            "expected_good_conditional_result": {
                "arithmetic": "exact joint for the declared tables",
            },
            "expected_safe_status": "refuse mixed-origin real output, or keep whole output test-only/unverified; never emit real-use authority for an unverified source",
            "expected_actual_pre_repair": {
                "accepted": True,
                "decision": "INFERRED_CANDIDATE_REQUIRES_REVIEW",
                "test_origin": False,
                "callback_invocations_for_real_source": 2,
                "callback_invocations_for_declared_test_source": 0,
                "native_authority_ceiling": "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P6_MISSING_OWNER_FAIL_CLOSED",
            "world": "F6L_P11_COMPLETE_POSITIVE",
            "question": "With real sources and admit=None, does the producer still fail closed?",
            "expected_good_conditional_result": {
                "arithmetic": "no output; refusal is correct",
            },
            "expected_safe_status": "SynthesisError, no candidate, no authority graph",
            "expected_actual_pre_repair": {
                "raises_SynthesisError": True,
            },
            "expected_actual_is_unsafe": False,
        },
        {
            "id": "P7_MAPPED_NODE_AUTHORITY_CEILING",
            "world": "F6L_P11_COMPLETE_POSITIVE",
            "question": "Does every mapped:* graph node retain authority_ceiling/provenance and no more privilege than its native parent?",
            "expected_good_conditional_result": {
                "arithmetic": "complete positive joint remains exact",
            },
            "expected_safe_status": "every node has authority_ceiling + provenance; mapped ceiling <= native; target_joint <= parents; test-only output never claims real use",
            "expected_actual_pre_repair": {
                "mapped_nodes_missing_authority_ceiling": True,
                "mapped_nodes_missing_value_hash": True,
                "test_only_native_ceiling": "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P8_DISTRIBUTED_SUPPORT_MINORITY",
            "world": "F6L_P8_DISTRIBUTED_SUPPORT_MINORITY",
            "question": "Is minimum_raw_support a total-stratum gate rather than a minority-cell guard, and when it excludes a source is the exclusion surfaced as bounded/partial consequence instead of silent renormalization?",
            "expected_good_conditional_result": {
                "min_1_joint": "7/50, 9/25, 1/4, 1/4",
                "min_5_joint_equals_min_1": True,
                "minority_cell_n": 3,
                "minority_cell_survives_threshold_5": True,
                "min_150_excludes": "S1",
                "min_150_silent_renormalization_is_unsafe": True,
            },
            "expected_safe_status": "truthful total-stratum naming; when S1 is excluded, do not present the S2-only complete joint as a complete target joint without a bound/status consequence",
            "expected_actual_pre_repair": {
                "min_1_decision": "SYNTHETIC_CANDIDATE",
                "min_5_decision": "SYNTHETIC_CANDIDATE",
                "min_150_decision": "SYNTHETIC_CANDIDATE",
                "min_150_distribution": "1/4,1/4,1/4,1/4",
                "min_150_uncovered_target_mass": "0",
                "min_150_excluded_sources": ["S1"],
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P9_STATUS_VS_ACTUAL_DISTRIBUTION",
            "world": "F6L_P2_NOVEL_2X2_UNCOVERED_THIRD",
            "question": "Can a decision-only downstream consumer mistake a null distribution for a complete candidate?",
            "expected_good_conditional_result": {
                "distribution": None,
                "covered_subprobability_sum": "2/3",
            },
            "expected_safe_status": "decision-only consumer must not read a complete candidate; status must agree with candidate.distribution is None",
            "expected_actual_pre_repair": {
                "decision": "SYNTHETIC_CANDIDATE",
                "decision_only_consumer": "CONSUMED_AS_COMPLETE",
                "distribution_reader_consumer": "NO_COMPLETE_TARGET_JOINT",
            },
            "expected_actual_is_unsafe": True,
        },
        {
            "id": "P10_ARITHMETIC_SOURCE_SUBSTITUTION",
            "world": "F6L_P10_SOURCE_SUBSTITUTION",
            "question": "Does substituting one source table move the exact joint to the independently recomputed target without moving identities or weights?",
            "expected_good_conditional_result": {
                "exact_joint": "5/16, 3/16, 3/16, 5/16",
                "differs_from_P11": True,
            },
            "expected_safe_status": "exact rational arithmetic follows the actual substituted source bytes; no stale/overwritten table",
            "expected_actual_pre_repair": {
                "expected_to_match": True,
            },
            "expected_actual_is_unsafe": False,
        },
        {
            "id": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
            "world": "F6L_P11_COMPLETE_POSITIVE",
            "question": "Does a genuinely positive complete target still yield a complete exact joint, supported consumer and non-null distribution?",
            "expected_good_conditional_result": {
                "exact_joint": "1/3, 1/6, 1/6, 1/3",
                "covered_sum": "1",
                "uncovered_target_mass": "0",
                "exact_lower": "1/6, 1/6, 1/6, 1/6",
                "exact_upper": "1/2, 1/6, 1/6, 1/2",
                "conditional_yes_given_low": "1/3",
                "consumer_state": "SUPPORTED_MODEL",
            },
            "expected_safe_status": "complete target joint remains available; useful positive result must not be suppressed",
            "expected_actual_pre_repair": {
                "decision": "SYNTHETIC_CANDIDATE",
                "distribution_present": True,
                "consumer_state": "SUPPORTED_MODEL",
            },
            "expected_actual_is_unsafe": False,
        },
    ]

    payload = {
        "schema": "PYAT_R28_F6L_PHASE_A_PREREGISTRATION@1",
        "role": "independent F6J scientific reviewer continuation (F6L); not F6K author, not HQ",
        "repository": "maidiu/rawlsing",
        "branch": "agent/reviewer-pyat-r28-f6l-independent-f6k-frozen-consumer-court-r1",
        "sealed_startup": "31123f370af50bdf036cab32dd6d7594b36a5f22",
        "native_under_test": {
            "commit": "1428c2e92bce1a49efd87378cb23df936d646dc5",
            "producer_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
            "empirical_objects_blob": "a61365b994e5c3c50de0f598fcf40e90abf757b6",
            "candidate_context": "9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f",
            "f6j_review": "825b2d8050b550f1d52d3129883584fee2ef36c2",
            "f6j_freeze": "e476ccc090ae0175a540e94c5c382d7e2a8453f0",
        },
        "ordering_attestation": {
            "f6k_candidate_read_before_this_freeze": False,
            "f6k_report_read_before_this_freeze": False,
            "native_imported_by_expectation_engine": False,
            "native_executed_by_build_script": False,
            "basis": "F6J/F6C public returns and the pinned native bytes only",
        },
        "worlds": worlds,
        "cases": cases,
        "decision_policy_preregistered": {
            "complete_allowed_only_when": "candidate.distribution is not None and uncovered_target_mass == 0",
            "forbidden_on_null_distribution": ["SYNTHETIC_CANDIDATE"],
            "safe_incomplete_markers": ["PARTIAL", "NO_COMPLETE", "INCOMPLETE", "BACKOFF", "UNIDENTIFIED"],
            "real_source_authority_from_unverified_callback": "FORBIDDEN",
            "test_origin_self_declaration": "NEVER_AUTHENTICATES_REAL_SOURCE",
        },
        "method_boundary": {
            "sourcefree_only": True,
            "no_original_measured_f6": True,
            "no_N9_OC05_N11_N12_actor": True,
            "no_person_or_cross_survey_link": True,
        },
    }

    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    OUT.write_text(text)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    print(f"wrote {OUT}")
    print(f"sha256 {digest}")
    for w in worlds:
        e = w["exact_expectations"]
        print(f"{w['case']:58s} covered={e['covered_subprobability_sum']:>5s} "
              f"uncovered={e['uncovered_target_mass']:>5s} complete={e['distribution_is_complete']}")
    print("conditional P11", [w for w in worlds if w["case"].startswith("P11")][0]
          ["exact_expectations"].get("exact_conditional_yes_given_low"))


if __name__ == "__main__":
    main()
