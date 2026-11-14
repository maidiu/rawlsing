#!/usr/bin/env python3
"""ZAK-02S historical-function S2 sourcefree witness.

No historical function bodies are copied or rewritten. The separate *legacy*
checkout is the exact 9253064... commit; this runner imports those modules
and verifies their Git blobs before invoking them.

Usage:
 python WORKER_RETURNS/ZAK02S_LEGACY_EXECUTION_20261114/run_historical.py \
   --legacy /path/to/legacy-checkout --out /path/to/results.json
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
import sys
import traceback

PIN = "9253064bc9423a0f0ccda4fbdea43c2f54f800c6"
BLOBS = {
    "ddm_v550_question_use.py": "8d90a5116fd05b5db17e9b4645638a3aa6fc1131",
    "ddm_v550j_joint_patterns.py": "644aab23675b26134040d1df5cc25538b613e163",
    "ddm_v551j_packets.py": "740bae4cfd4da7ed8aa2c9a2321c47f26ba7c7e8",
    "ddm_v552_structural.py": "0df56d70cb3880dee723df00aea2207acd525260",
    "ddm_v552j_handoff.py": "476e617370e8947ee1f38b0718243ecfc5ba9e5c",
    "build_question_response_attitude_cloud_summary_v549b.py": "bf874a95ea5172817b0d1bdf21b43600aac5cbfe",
}
ROOT = "data/ddm_build_copy/"
RESULTS = []


def git(legacy: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(legacy), *args], text=True).strip()


def observe(name, phase, symbol, inputs, invoke, check):
    try:
        value = invoke()
        observation = {"return": value}
    except Exception as exc:
        observation = {
            "exception_type": type(exc).__name__,
            "exception": str(exc),
            "traceback_tail": traceback.format_exc(limit=3).strip()[-1200:],
        }
    try:
        ok = bool(check(observation))
    except Exception as exc:
        ok = False
        observation["expectation_error"] = repr(exc)
    RESULTS.append({
        "case": name, "phase": phase, "symbol": symbol,
        "synthetic_inputs": inputs, "observed": observation,
        "check_pass": ok, "grade": "S2_SYNTHETIC_PINNED_FUNCTION",
        "historical_original_production": False,
    })
    print(("PASS " if ok else "FAIL ") + name + ":" + phase, flush=True)
    return observation


def invoke_550j(module, pd, member_ids):
    respondents = pd.DataFrame([
        {"respondent_id": "R1", "var_code": "ATTITUDE", "response_value_normalized": "YES",
         "allowed_as_association_feature": True, "weight_value": 1.0},
        {"respondent_id": "R2", "var_code": "ATTITUDE", "response_value_normalized": "NO",
         "allowed_as_association_feature": True, "weight_value": 1.0},
    ])
    members = pd.DataFrame([
        {"run_id": "SYN", "source_id": "SYN", "source": "GSS", "wave": "1973",
         "canonical_wave": "1973", "country_code": "US", "family_id": "FAM",
         "pattern_id": "P", "respondent_id_norm": rid,
         "pattern_count_unweighted": len(member_ids),
         "pattern_count_weighted": float(len(member_ids)),
         "pattern_support_status": "supported",
         "confidence_score": 1.0, "weight_value": 1.0}
        for rid in member_ids
    ])
    trace = module._association_candidate_trace_rows_fast(
        pd.DataFrame([{"pattern_id": "P"}]), respondents,
        pattern_membership_frame=members,
        association_support_threshold=1, emit_diagnostics=True,
        run_id="SYN", source_id="SYN", source="GSS", wave="1973",
        canonical_wave="1973", country_code="US",
    )
    if trace is None or trace.empty:
        return {"rows": 0, "candidates": []}
    return {"rows": len(trace), "candidates": [
        {key: row.get(key) for key in (
            "associated_response_value", "n_overlap_unweighted",
            "baseline_answered_n_unweighted", "pattern_answered_var_n_unweighted",
            "p_response_given_pattern", "p_response_baseline",
            "denominator_basis", "baseline_denominator_basis", "association_publication_status",
        )}
        for row in trace.to_dict("records")
    ]}


def invoke_551j(module, pd, mode):
    pattern = {
        "pattern_count_unweighted": 3, "support_score": 1.0,
        "support_status": "supported", "support_gate_status": "sufficient_support",
        "registry_resolved_share": 1.0,
    }
    base = {
        "v551_atom_match_status": "MATCHED_EXACT_ATOM",
        "cross_contract_status": "EXACT_MATCH",
        "component_certification_contribution": "relation_component",
        "v550j_item_response_semantics_authority_status": "CERTIFIED",
        "v550j_item_directionality_authority_status": "CERTIFIED",
        "v550j_target_resolution_status": "resolved",
        "v551_structural_mapping_status": "complete",
        "v550j_item_response_direction": "positive",
    }
    rows = [dict(base), dict(base)]
    if mode == "unexplained":
        # Keep two genuine relation components so the unresolved-component
        # blocker is isolated from the independent insufficient-relations gate.
        rows.append({**base, "component_certification_contribution": "unresolved_component"})
    if mode == "ambiguous":
        rows[1]["v551_atom_match_status"] = "AMBIGUOUS_V551_ATOM_MATCH"
    if mode == "conflict":
        rows[1]["cross_contract_status"] = "VALUE_CONFLICT"
    if mode == "unexplained":
        rows[1]["component_certification_contribution"] = "unresolved_component"
    if mode == "insufficient":
        rows[1]["component_certification_contribution"] = "context_component"
    if mode == "authority_gap":
        rows[1]["v550j_item_directionality_authority_status"] = "REVIEW_REQUIRED"
    if mode == "measurement_gap":
        pattern.pop("support_score")
    status, evidence_class, reviews, blockers, authority = module._v2_packet_status(
        pattern, pd.DataFrame(rows), {"target_structure_status": "resolved"}
    )
    return {"status": status, "evidence_class": evidence_class,
            "reviews": reviews, "blockers": blockers, "authority": authority}


def invoke_552(module, pd, counts):
    comp = pd.DataFrame([
        {"empirical_distribution_id": "DIST", "source_atom_id": f"A{i}",
         "source_atom_contract_hash": f"H{i}", "source_measurement_contract_hash": f"M{i}",
         "response_value_normalized": str(i), "v551_signed_side": 1,
         "v551_signed_intensity": 0.5, "n_respondents": 2,
         "n_unweighted": n, "pct_unweighted": n / sum(counts),
         "canonical_signed_component": 0.5, "component_pressure_eligible": True,
         "canonical_signed_component_zero": False}
        for i, n in enumerate(counts)
    ])
    coverage = pd.DataFrame([{"empirical_distribution_id": "DIST",
                               "directional_adjudication_status": "COMPLETE"}])
    atoms = pd.DataFrame([{"empirical_distribution_id": "DIST", "source": "GSS",
                           "source_family": "GSS", "wave": "1973", "canonical_wave": "1973",
                           "country_code": "US", "question_id": "Q", "var_code": "VAR",
                           "analysis_scope": "SYN", "empirical_object_type": "survey_response"}])
    surface = module._surface(comp)
    full = module.build_v552_pressure_observation_index(
        atoms, comp, coverage, pd.DataFrame(), run_id="SYN"
    )
    row = full.iloc[0].to_dict()
    return {"surface": {"status": surface[0], "coverage": surface[1],
                         "basis": surface[2]},
            "pressure_score_status": row.get("pressure_score_status"),
            "pressure_score": row.get("pressure_score"),
            "downstream_permission_status": row.get("downstream_permission_status"),
            "response_surface_completeness_status": row.get("response_surface_completeness_status")}


def invoke_552j(module, pd, fact_ids, flip=False, mismatched=False):
    packet = {"run_id": "SYN", "source": "GSS", "canonical_wave": "1973",
              "country_code": "US", "packet_id": "PACKET",
              "relation_axis_id": "REL", "target_entity_id": "TGT",
              "driver_facet_id": "FACET", "question_id": "QUESTION"}
    facts = [{
        "run_id": "OTHER" if mismatched else "SYN", "source": "GSS",
        "canonical_wave": "1973", "country_code": "US",
        "v552_structural_fact_id": fid, "relation_axis_id": "REL",
        "target_entity_id": "TGT", "driver_facet_id": "FACET",
        "question_id": "QUESTION", "pressure_score_status": "OBSERVED_NONZERO",
        "pressure_score": 0.5, "measurement_evidence_status": "PRESENT",
        "downstream_permission_status": "ALLOW", "source_artifact": "SYNTHETIC",
    } for fid in fact_ids]
    if flip:
        facts.reverse()
    frame = pd.DataFrame(facts)
    resolution = module._packet_structural_dimension_resolution(
        pd.Series(packet), frame, pd.DataFrame()
    )
    full = module.build_v552j_join(
        run_id="SYN", v551j_certified=pd.DataFrame([packet]),
        v551j_review=pd.DataFrame(), v552_structural_facts=frame,
        v551j_state={"evidence_status": "PRESENT", "downstream_permission_status": "ALLOW"},
        v552_state={"evidence_status": "PRESENT", "downstream_permission_status": "ALLOW"},
    )
    selected = full["join_index"]
    return {"selected_fact_id": resolution["source_v552_structural_fact_id"],
            "match_score": resolution["v552_structural_match_score"],
            "matched_fact_count": resolution["matched_fact_count"],
            "resolution_status": resolution["resolution_status"],
            "joined_fact_ids": [] if selected.empty else selected["v552_structural_fact_id"].tolist(),
            "join_permissions": [] if selected.empty else selected["join_permission"].tolist(),
            "join_audit": full["join_audit"]["join_status"].tolist()}


def invoke_549b(module, pd, n_candidates, reporter):
    import numpy as np
    n = 120
    src = {"BIN": [1] * 60 + [0] * 60}
    candidates = [{"item_id": "SYN:1973:BIN", "question_type": "multi_select",
                   "final_driver_id": "SYNDRV"}]
    for i in range(1, n_candidates):
        var = f"Q{i:02d}"
        src[var] = [0, 1] * 60 if i % 2 else [1, 0] * 60
        candidates.append({"item_id": f"SYN:1973:{var}",
                           "question_type": "single_choice", "final_driver_id": "SYNDRV"})
    anchors, rows, exclusions = module.build_answer_presence_anchors(
        "SYN", "1973", "US", pd.DataFrame({"respondent_id": list(range(n))}),
        pd.DataFrame(src), pd.DataFrame(candidates),
        module.ProgressReporter(interval_seconds=99999) if reporter else None,
    )
    return {"anchors": len(anchors), "rows": len(rows),
            "exclusions": len(exclusions), "candidates": n_candidates,
            "reporter": reporter}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    legacy = args.legacy.resolve()
    actual = git(legacy, "rev-parse", "HEAD")
    if actual != PIN:
        raise RuntimeError(f"historical checkout mismatch: {actual} != {PIN}")
    actual_blobs = {name: git(legacy, "hash-object", ROOT + name) for name in BLOBS}
    if actual_blobs != BLOBS:
        raise RuntimeError(f"historical blob mismatch: {actual_blobs}")
    sys.path.insert(0, str(legacy))
    import pandas as pd
    mods = {}
    for short in BLOBS:
        name = short.removesuffix(".py")
        dotted = f"data.ddm_build_copy.{name}"
        module = importlib.import_module(dotted)
        expected = (legacy / ROOT / short).resolve()
        if Path(module.__file__).resolve() != expected:
            raise RuntimeError(f"not historical import {dotted}: {module.__file__}")
        mods[name] = module

    f08 = mods["ddm_v550_question_use"]
    record = {"source": "GSS", "wave": "1973", "canonical_wave": "1973",
              "var_code": "USWAR", "question_id": "Q-USWAR"}
    # Disjoint selector keys: A matches the variable-code basis only,
    # B matches the question-ID basis only. This isolates the distinct-identity
    # refusal instead of accidentally testing duplicate question matches.
    row_a = {**record, "question_id": "Q-ALT", "override_id": "A"}
    row_b = {**record, "var_code": "OTHER", "override_id": "B"}
    def sel(frame):
        chosen, basis, _ = f08._select_override(record, pd.DataFrame(frame))
        return {"override_id": None if chosen is None else chosen.get("override_id"),
                "basis": basis}
    observe("F08", "positive", "_select_override", {"record": record, "overrides": [row_a]},
            lambda: sel([row_a]), lambda o: o.get("return", {}).get("override_id") == "A")
    observe("F08", "negative_conflicting_matches", "_select_override",
            {"record": record, "overrides": [row_a, row_b]},
            lambda: sel([row_a, row_b]),
            lambda o: o.get("exception_type") == "RuntimeError" and "matched multiple distinct override rows" in o.get("exception", ""))
    observe("F08", "negative_duplicate", "_select_override",
            {"record": record, "overrides": [row_a, row_a]},
            lambda: sel([row_a, row_a]), lambda o: o.get("exception_type") == "RuntimeError")
    observe("F08", "negative_unmatched", "_select_override",
            {"record": record, "overrides": [{**row_a, "wave": "1980", "canonical_wave": "1980"}]},
            lambda: sel([{**row_a, "wave": "1980", "canonical_wave": "1980"}]),
            lambda o: o.get("return", {}).get("override_id") is None)
    observe("F08", "restore", "_select_override", {"record": record, "overrides": [row_a]},
            lambda: sel([row_a]), lambda o: o.get("return", {}).get("override_id") == "A")

    joint = mods["ddm_v550j_joint_patterns"]
    sym = "_association_candidate_trace_rows_fast"
    observe("V550J", "positive_same_respondent", sym,
            {"baseline": [["R1", "YES"], ["R2", "NO"]], "members": ["R1"]},
            lambda: invoke_550j(joint, pd, ["R1"]),
            lambda o: any(x["associated_response_value"] == "YES"
                          and x["n_overlap_unweighted"] == 1
                          and x["baseline_answered_n_unweighted"] == 2
                          and x["pattern_answered_var_n_unweighted"] == 1
                          and x["denominator_basis"] == "answered_var_within_pattern"
                          and x["baseline_denominator_basis"] == "eligible_context"
                          for x in o.get("return", {}).get("candidates", [])))
    observe("V550J", "negative_disjoint_respondents", sym,
            {"baseline": [["R1", "YES"], ["R2", "NO"]], "members": ["R3"]},
            lambda: invoke_550j(joint, pd, ["R3"]),
            lambda o: o.get("return", {}).get("rows") == 0)
    observe("V550J", "restore", sym,
            {"baseline": [["R1", "YES"], ["R2", "NO"]], "members": ["R1"]},
            lambda: invoke_550j(joint, pd, ["R1"]),
            lambda o: any(x["n_overlap_unweighted"] == 1 for x in o.get("return", {}).get("candidates", [])))

    packets = mods["ddm_v551j_packets"]
    sym = "_v2_packet_status"
    observe("V551J", "positive", sym, {"components": 2, "mode": "valid"},
            lambda: invoke_551j(packets, pd, "valid"),
            lambda o: o.get("return", {}).get("status", "").startswith("CERTIFIED_JOINT"))
    for mode, expectation in [
        ("ambiguous", "BLOCKED_AMBIGUOUS_COMPONENT_MATCH"),
        ("conflict", "BLOCKED_CROSS_CONTRACT_CONFLICT"),
        ("unexplained", "BLOCKED_PACKET_CONTRACT"),
        ("insufficient", "CONTEXT_ONLY_PATTERN"),
        ("authority_gap", "REVIEW_REQUIRED_AUTHORITY_GAP"),
        ("measurement_gap", "REVIEW_REQUIRED_COMPONENT_GAP"),
    ]:
        observe("V551J", "negative_" + mode, sym, {"components": 2, "mode": mode},
                lambda mode=mode: invoke_551j(packets, pd, mode),
                lambda o, expectation=expectation: o.get("return", {}).get("status") == expectation)
    observe("V551J", "restore", sym, {"components": 2, "mode": "valid"},
            lambda: invoke_551j(packets, pd, "valid"),
            lambda o: o.get("return", {}).get("status", "").startswith("CERTIFIED_JOINT"))

    structural = mods["ddm_v552_structural"]
    sym = "_surface + build_v552_pressure_observation_index"
    observe("V552", "positive_coverage_and_score", sym, {"selected_counts": [1, 1], "denominator": 2},
            lambda: invoke_552(structural, pd, [1, 1]),
            lambda o: o.get("return", {}).get("surface", {}).get("status") == "COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE"
            and o["return"]["downstream_permission_status"] == "ALLOW"
            and o["return"]["pressure_score_status"] == "OBSERVED_NONZERO")
    observe("V552", "negative_overcount_but_score_independent", sym,
            {"selected_counts": [2, 2], "denominator": 2},
            lambda: invoke_552(structural, pd, [2, 2]),
            lambda o: o.get("return", {}).get("surface", {}).get("status") == "BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR"
            and o["return"]["surface"]["coverage"] == 2.0
            and o["return"]["downstream_permission_status"] == "ALLOW")
    observe("V552", "restore", sym, {"selected_counts": [1, 1], "denominator": 2},
            lambda: invoke_552(structural, pd, [1, 1]),
            lambda o: o.get("return", {}).get("surface", {}).get("status") == "COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE")

    handoff = mods["ddm_v552j_handoff"]
    sym = "_packet_structural_dimension_resolution + build_v552j_join"
    observe("V552J", "positive_single_fact", sym, {"facts": ["FACT_A"]},
            lambda: invoke_552j(handoff, pd, ["FACT_A"]),
            lambda o: o.get("return", {}).get("selected_fact_id") == "FACT_A"
            and o["return"]["joined_fact_ids"] == ["FACT_A"])
    for phase, flip in [("negative_equal_score_twin", False), ("negative_permuted_twin", True)]:
        observe("V552J", phase, sym, {"facts": ["FACT_A", "FACT_Z"], "reverse_input": flip},
                lambda flip=flip: invoke_552j(handoff, pd, ["FACT_A", "FACT_Z"], flip=flip),
                lambda o: o.get("return", {}).get("selected_fact_id") == "FACT_Z"
                and o["return"]["matched_fact_count"] == 2
                and o["return"]["joined_fact_ids"] == ["FACT_Z"])
    observe("V552J", "negative_wrong_run", sym, {"facts": ["FACT_A"], "mismatched_run": True},
            lambda: invoke_552j(handoff, pd, ["FACT_A"], mismatched=True),
            lambda o: o.get("return", {}).get("selected_fact_id") == ""
            and o["return"]["joined_fact_ids"] == [])
    observe("V552J", "restore", sym, {"facts": ["FACT_A"]},
            lambda: invoke_552j(handoff, pd, ["FACT_A"]),
            lambda o: o.get("return", {}).get("selected_fact_id") == "FACT_A")

    reporter = mods["build_question_response_attitude_cloud_summary_v549b"]
    sym = "build_answer_presence_anchors"
    observe("V549b", "positive_under_threshold", sym,
            {"candidates": 49, "progress_item_step": 50, "reporter": True},
            lambda: invoke_549b(reporter, pd, 49, True),
            lambda o: o.get("return", {}).get("anchors", 0) >= 1)
    observe("V549b", "negative_conditional_50th_report", sym,
            {"candidates": 50, "progress_item_step": 50, "reporter": True},
            lambda: invoke_549b(reporter, pd, 50, True),
            lambda o: o.get("exception_type") == "NameError"
            and ("answer_type" in o.get("exception", "") or "cand_item_id" in o.get("exception", "")))
    observe("V549b", "restore_without_reporter", sym,
            {"candidates": 50, "reporter": False},
            lambda: invoke_549b(reporter, pd, 50, False),
            lambda o: o.get("return", {}).get("anchors", 0) >= 1)

    import numpy
    summary = {"source_commit": PIN, "source_blobs": actual_blobs,
               "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "environment": {"python": sys.version.split()[0], "pandas": pd.__version__,
                               "numpy": numpy.__version__},
               "cases": RESULTS, "total": len(RESULTS),
               "pass": sum(int(x["check_pass"]) for x in RESULTS),
               "fail": sum(int(not x["check_pass"]) for x in RESULTS),
               "first_consumers": {
                   "F08": "not executed; inspect V550 contract builder",
                   "V550J": "compile_v551j_joint_evidence_packets.py named callsite only",
                   "V551J": "compile_v551j_joint_evidence_packets.py named callsite only",
                   "V552": "compile_v552j_structural_handoff.py named callsite only",
                   "V552J": "compile_v552j_structural_handoff.py named callsite only",
                   "V549b": "historical non-test downstream reader unverified",
               },
               "original35_native": False, "independent_receiving": False,
               "protected_merge": False}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(summary, sort_keys=True, indent=2, default=str) + "\n")
    print("ZAK02S_JSON_BEGIN", flush=True)
    print(json.dumps({"total": summary["total"], "pass": summary["pass"],
                      "fail": summary["fail"], "results": [
                         {"case": x["case"], "phase": x["phase"], "pass": x["check_pass"],
                          "observed": x["observed"].get("return", {
                              "exception_type": x["observed"].get("exception_type"),
                              "exception": x["observed"].get("exception")})}
                         for x in RESULTS]}, separators=(",", ":"), default=str), flush=True)
    print("ZAK02S_JSON_END", flush=True)
    return 0 if summary["fail"] == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as fatal:
        # Preserve exact import/checkout/schema blockers as machine-readable
        # evidence too. A fatal preflight is NOT a passed or attempted case.
        payload = {
            "source_commit_expected": PIN,
            "result": "NOT_RUN_FATAL_PREFLIGHT",
            "fatal_exception_type": type(fatal).__name__,
            "fatal_exception": str(fatal),
            "traceback": traceback.format_exc(),
            "cases_completed_before_fatal": RESULTS,
            "passed_cases": sum(int(c["check_pass"]) for c in RESULTS),
            "unexecuted_operational_families": sorted({"F08", "V550J", "V551J", "V552", "V552J", "V549b"} - {c["case"] for c in RESULTS}),
        }
        if "--out" in sys.argv and sys.argv.index("--out") + 1 < len(sys.argv):
            target = Path(sys.argv[sys.argv.index("--out") + 1])
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str) + "\n")
        print("ZAK02S_FATAL_PREFLIGHT " + json.dumps(payload, default=str), flush=True)
        raise
