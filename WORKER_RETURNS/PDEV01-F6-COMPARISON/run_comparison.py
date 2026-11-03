"""PDEV-01 F6 receiver comparison: F6P evidence -> current WP2 receiver contract."""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
F6P = ROOT / "stage/F6P/WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1"
for path in (F6P, F6P / "native", F6P / "oracle", F6P / "tests"):
    sys.path.insert(0, str(path))

from f6p_fixtures import build, request  # noqa: E402
import f6p_partial_bound_evidence_consumer as C  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402


def summarize(world: str):
    bundle = build("B", world)
    result = C.consume_f6m_evidence(bundle, request(world))
    return {
        "world": world,
        "bundle_decision": bundle.get("decision"),
        "target_joint_status": bundle.get("target_joint_status"),
        "uncovered_target_mass": result.get("uncovered_target_mass"),
        "covered_subprobability": result.get("covered_subprobability"),
        "evidence_state": result.get("evidence_state"),
        "evidence_reasons": result.get("evidence_reasons"),
        "supported_point": result.get("supported_point"),
        "bounds": result.get("bounds"),
        "exclusions": result.get("exclusions"),
        "sampling": result.get("sampling"),
        "transport": result.get("transport"),
        "real_use_authorized": result.get("real_use_authorized"),
        "no_route_probability": result.get("no_route_probability"),
        "no_selection_weight": result.get("no_selection_weight"),
        "output_hash": result.get("output_hash"),
        "consumer_id": result.get("consumer_id"),
        "source_product": result.get("source_product"),
    }


def current_wp2_f6_sidecar(value):
    """Exact WP2 transport expression at c1ebe091f / wp2.py line 94.

    The current WP2 envelope constructs F6 sidecars from F6M's native bundle
    and native conditional consumer.  It has no F6P evidence branch.
    """
    return {
        "bundle_hash": value["native_bundle"]["content_hash"],
        "conditional": value["native_conditional_consumer"],
    }


def main():
    worlds = ["W1_full_coverage_disjoint", "W2_mixed_eligibility_trap",
              "W7_source_excluded_all_strata", "W3_minority_whole_stratum_absent"]
    results = {world: summarize(world) for world in worlds}
    f6p_w2 = build("B", "W2_mixed_eligibility_trap")
    f6p_result = C.consume_f6m_evidence(f6p_w2, request("W2_mixed_eligibility_trap"))
    try:
        current_wp2_f6_sidecar(f6p_result)
        mismatch = {"raw_exception_observed": False}
    except KeyError as exc:
        # The candidate comparison harness, not F6P or WP2, labels this
        # boundary condition.  Preserve the receiver's raw exception.
        mismatch = {
            "raw_exception_observed": True,
            "raw_exception_type": type(exc).__name__,
            "raw_exception_args": list(exc.args),
            "raw_exception_str": str(exc),
            "expected_receiver_fields": ["native_bundle", "native_conditional_consumer"],
            "supplied_f6p_fields": sorted(f6p_result.keys()),
            "first_missing_field": "native_bundle",
            "receiver_pin": {
                "wp2_commit": "f7824794bc6674c662734c9a8b110dd3df224be7",
                "wp2_blob": "55e567e4d0780c251bf949268d3d477abdc76a9b",
                "wp2_line": 94,
            },
            "wp2_receiver_executed": False,
            "observed_effect": None,
            "authored_diagnostic_label": "COMPARISON_LOCAL_BOUNDARY_SHAPE_DIFFERENCE__NOT_EMITTED_BY_F6P_OR_WP2",
            "authored_diagnostic_location": "run_comparison.py:current_wp2_f6_sidecar",
        }
    refused = {}
    for key in ("REAL_USE", "TRANSPORT_PERMISSION", "ADMISSION"):
        req = request("W2_mixed_eligibility_trap")
        if key == "REAL_USE":
            req["use"] = "REAL_USE"
        elif key == "TRANSPORT_PERMISSION":
            req["transport_permission"] = "OWNER_APPROVED"
        else:
            req["admission"] = "OWNER_APPROVED"
        r = C.consume_f6m_evidence(build("B", "W2_mixed_eligibility_trap"), req)
        refused[key] = {"evidence_state": r["evidence_state"],
                        "evidence_reasons": r["evidence_reasons"],
                        "supported_point": r["supported_point"]}
    severed = build("B", "W2_mixed_eligibility_trap")
    severed["candidate"] = None
    severed["decision"] = "SOURCE_INDEXED_BACKOFF"
    severed["target_joint_status"] = "NO_COMPLETE_TARGET_JOINT"
    severed["content_hash"] = semantic_hash({k: v for k, v in severed.items() if k != "content_hash"})
    severed_result = C.consume_f6m_evidence(severed, request("W2_mixed_eligibility_trap"))
    document = {
        "schema": "PDEV01_F6_RECEIVER_COMPARISON@1.0.0",
        "source_pins": {
            "f6p_commit": "7d7ed1cb01bfd32383ee487996d2595c666a07b2",
            "f6p_consumer_blob": "8fa992899293f454d7abded36831a4b4a362df8e",
            "f6m_repair_review": "9b885d80be83c25295b3b43a5ece705c4e5c2fbb",
            "f6m_candidate_blob": "2df811d76db258d98d89ffb43c830cb221ff9a7d",
            "f6m_corrected_A_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
            "f6m_A0_blob": "182cc7970d7624f6614015f5a51d0602e1630d52",
            "f6p_independent_review": "2e00c8c9e9f2d5f78e40ebfedc2f4468dd97edec",
            "f6c_commit": "c1ebe091fa2bd12b254e5599cf37975fe438d462",
            "wp2_commit": "f7824794bc6674c662734c9a8b110dd3df224be7",
            "wp2_blob": "55e567e4d0780c251bf949268d3d477abdc76a9b",
        },
        "actual_first_consumer": {
            "symbol": "f6p_partial_bound_evidence_consumer.consume_f6m_evidence",
            "file": "WORKER_RETURNS/PYAT-R39-F6P-PARTIAL-BOUND-EVIDENCE-CONSUMER-R1/f6p_partial_bound_evidence_consumer.py",
            "line": 189,
            "grade": "SOURCEFREE_TEST_ONLY",
            "receives": "actual repaired F6M bundle plus request",
            "does_not_receive": "current WP2/N9 selected-world route input",
        },
        "current_receiver": {
            "symbol": "wp2.product() f6_products -> generic_read_only_input.f6_sidecars",
            "commit": "f7824794bc6674c662734c9a8b110dd3df224be7",
            "blob": "55e567e4d0780c251bf949268d3d477abdc76a9b",
            "line": 94,
            "grade": "UNINSTALLED_TEST_ONLY_PORT",
            "named_receiver": "NONPARENT_OPTIONS generic read-only world input port",
            "join_state": "NO_AUTHORIZED_COMMON_WORLD_OR_RESPONDENT_JOIN",
        },
        "results": results,
        "receiver_shape_check": mismatch,
        "refusals": refused,
        "severance": {
            "candidate_removed": True,
            "evidence_state": severed_result["evidence_state"],
            "evidence_reasons": severed_result["evidence_reasons"],
            "supported_point": severed_result["supported_point"],
            "uncovered_target_mass": severed_result["uncovered_target_mass"],
        },
        "conclusion": {
            "partial_bounds_reach_f6p_consumer": all(
                results[w]["evidence_state"] == "PARTIAL_IDENTIFICATION"
                and results[w]["supported_point"] is None
                for w in ("W2_mixed_eligibility_trap", "W7_source_excluded_all_strata", "W3_minority_whole_stratum_absent")),
            "partial_bounds_reach_current_wp2_receiver": False,
            "wp2_receiver_executed": False,
            "raw_exception": {
                "type": mismatch.get("raw_exception_type"),
                "args": mismatch.get("raw_exception_args"),
                "str": mismatch.get("raw_exception_str"),
            },
            "authored_diagnostic_label": mismatch.get("authored_diagnostic_label"),
            "reason": "F6P emits F6P_PARTIAL_BOUND_EVIDENCE; the exact WP2 sidecar expression expects F6M native_bundle + native_conditional_consumer. This is a structural shape check only; WP2 product() was not executed and no receiver effect is claimed.",
            "no_pooling": True,
            "point_refused_when_uncovered": all(
                results[w]["supported_point"] is None
                for w in ("W2_mixed_eligibility_trap", "W7_source_excluded_all_strata", "W3_minority_whole_stratum_absent")),
            "distinct_populations_preserved": True,
            "population_claim": False,
        },
    }
    (ROOT / "evidence" / "f6p-receiver-comparison.json").write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"schema": document["schema"],
                      "first": document["actual_first_consumer"]["symbol"],
                      "current": document["current_receiver"]["symbol"],
                      "mismatch": mismatch,
                      "conclusion": document["conclusion"]}, sort_keys=True))


if __name__ == "__main__":
    main()
