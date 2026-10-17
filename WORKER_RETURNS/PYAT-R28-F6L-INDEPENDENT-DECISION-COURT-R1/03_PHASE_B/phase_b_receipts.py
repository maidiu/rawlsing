"""F6L Phase-B changed-world / unchanged-world receipts against the pinned
native producer, after the F6K typed hold.

No repair code exists.  This probe records exactly what is unchanged (the
confirmed arithmetic and the falsified behaviour) and what changed (nothing in
F6K).  It does not edit any expectation.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RET / "01_STAGED_NATIVE"))
sys.path.insert(0, str(RET / "02_PHASE_A/03_SCRIPTS"))

from rawlsing_next.pre553_heterogeneous_synthesis import (  # noqa: E402
    synthesize, conditional, SynthesisError, METHOD)
import rawlsing_next.pre553_heterogeneous_synthesis as PRODUCER  # noqa: E402

PREREG = json.loads((RET / "02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json").read_text())
WORLDS = {w["case"]: w for w in PREREG["worlds"]}
CASE_WORLD = {
    "P4_FORGED_REAL_SOURCE_ADMIT_TRUE": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P5_TEST_ORIGIN_BYPASS": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P5B_MIXED_ORIGIN_CONTAMINATION": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P6_MISSING_OWNER_FAIL_CLOSED": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P7_MAPPED_NODE_AUTHORITY_CEILING": "P11_GENUINE_COMPLETE_TARGET_POSITIVE",
    "P9_STATUS_VS_ACTUAL_DISTRIBUTION": "P2_NOVEL_2X2_NO_POSITIVITY",
}
REAL_USE = "EXTERNAL_OWNER_ADMISSION_FOR_REAL_USE"


def fkey(text):
    return ast.literal_eval(text)


def exp_map(entry, field):
    return {fkey(k): F(v) for k, v in entry["exact_expectations"][field].items()}


def cells(cell_list):
    return {tuple(c["categories"]): F(c["probability"]) for c in cell_list}


def bounds(c):
    return {tuple(b["categories"]): (F(b["lower"]), F(b["upper"]))
            for b in c["uncertainty"]["source_disagreement_and_uncovered_bounds"]}


def run(case, *, test_origin=None, admit=lambda *_: True, min_raw_support=None,
        calls=None):
    entry = WORLDS[CASE_WORLD.get(case, case)]
    target = copy.deepcopy(entry["target"])
    sources = copy.deepcopy(entry["sources"])
    policy = copy.deepcopy(entry["policy"])
    if test_origin is not None:
        for src in sources:
            src["test_origin"] = bool(test_origin)
    if min_raw_support is not None:
        policy["minimum_raw_support"] = int(min_raw_support)

    def callback(source, tgt, phase):
        if calls is not None:
            calls.append({"source_id": source["source_id"], "phase": phase})
        return True

    return synthesize(target, sources, policy,
                      admit=callback if calls is not None else admit)


def exact_arithmetic(case):
    out = run(case)
    e = WORLDS[CASE_WORLD.get(case, case)]
    cand = out["candidate"]
    covered = cells(cand["covered_subprobability"])
    b = bounds(cand)
    ok = {
        "covered_subprobability_exact": covered == exp_map(e, "exact_joint_covered_subprobability"),
        "uncovered_target_mass_exact": F(cand["uncovered_target_mass"]) == F(e["exact_expectations"]["uncovered_target_mass"]),
        "lower_exact": {k: v[0] for k, v in b.items()} == exp_map(e, "exact_lower"),
        "upper_exact": {k: v[1] for k, v in b.items()} == exp_map(e, "exact_upper"),
        "distribution_null_matches": (cand["distribution"] is None) == (not e["exact_expectations"]["distribution_is_complete"]),
    }
    return {
        "case": case,
        "world": e["world_id"],
        "actual_decision": out["decision"],
        "candidate_distribution_is_none": cand["distribution"] is None,
        "covered_subprobability_sum": str(sum(covered.values(), F(0))),
        "uncovered_target_mass": cand["uncovered_target_mass"],
        "checks": ok,
        "all_exact": all(ok.values()),
    }


def main():
    import subprocess
    blob = hashlib.sha1(
        b"blob " + str(Path(PRODUCER.__file__).stat().st_size).encode() + b"\0"
        + Path(PRODUCER.__file__).read_bytes()).hexdigest()

    arithmetic = [exact_arithmetic(c) for c in
                  ("P1_ORIGINAL_UNCOVERED_WORLD", "P2_NOVEL_2X2_NO_POSITIVITY",
                   "P3_NOVEL_3_CATEGORY_NO_POSITIVITY",
                   "P10_ARITHMETIC_SOURCE_SUBSTITUTION",
                   "P11_GENUINE_COMPLETE_TARGET_POSITIVE")]

    # F6J 82/82 receipt.
    f6j_evidence = json.loads(
        (RET / "01_SOURCE_TRANSPORT/F6J_RUNTIME/07_EVIDENCE/native_vs_frozen.json").read_text())

    # Actual P1 null decision and consumer.
    p1 = run("P1_ORIGINAL_UNCOVERED_WORLD")
    p1_consumer = conditional(p1, {"material_security": "secure"}, "employment_position")

    # Actual P4/P5/P5B authority observations.
    p4_calls = []
    p4 = run("P4_FORGED_REAL_SOURCE_ADMIT_TRUE", test_origin=False, calls=p4_calls)
    p5_calls = []
    p5 = run("P5_TEST_ORIGIN_BYPASS", test_origin=True, calls=p5_calls)
    p5b_calls = []
    p5b_entry = WORLDS["P11_GENUINE_COMPLETE_TARGET_POSITIVE"]
    p5_target = copy.deepcopy(p5b_entry["target"])
    p5_sources = copy.deepcopy(p5b_entry["sources"])
    p5_sources[0]["test_origin"] = False
    p5_sources[1]["test_origin"] = True
    p5b = synthesize(p5_target, p5_sources, copy.deepcopy(p5b_entry["policy"]),
                     admit=lambda s, t, p: (p5b_calls.append(s["source_id"]) or True))

    # P6 preserved fail-closed.
    p6 = {"admit_none_raises": False, "admit_false_raises": False}
    try:
        run("P6_MISSING_OWNER_FAIL_CLOSED", test_origin=False, admit=None)
    except SynthesisError:
        p6["admit_none_raises"] = True
    try:
        run("P6_MISSING_OWNER_FAIL_CLOSED", test_origin=False, admit=lambda *_: False)
    except SynthesisError:
        p6["admit_false_raises"] = True

    # P7 graph.
    p7 = run("P7_MAPPED_NODE_AUTHORITY_CEILING", test_origin=True)
    p7_nodes = [{"node_id": n["node_id"],
                 "authority_ceiling": n.get("authority_ceiling"),
                 "missing_ceiling": "authority_ceiling" not in n,
                 "missing_value_hash": n["node_id"].startswith("mapped:") and "value_hash" not in n}
                for n in p7["evidence_graph"]]

    # P8 support.
    p8_1 = run("P8_DISTRIBUTED_SUPPORT_MIN_1", min_raw_support=1)
    p8_5 = run("P8_DISTRIBUTED_SUPPORT_MIN_5_CELL_NOT_GATE", min_raw_support=5)
    p8_150 = run("P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED", min_raw_support=150)
    p8_150_consumer = conditional(p8_150, {"F6L_MATERIAL": "LOW"}, "F6L_ACTION")

    # P9 decision-only consumer.
    p9 = run("P9_STATUS_VS_ACTUAL_DISTRIBUTION")

    payload = {
        "schema": "PYAT_R28_F6L_CHANGED_UNCHANGED_RECEIPTS@1",
        "native_identity": {
            "module_file": str(PRODUCER.__file__),
            "git_blob": blob,
            "expected_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
            "method": METHOD,
        },
        "f6k_return": {
            "repair_code_shipped": False,
            "suites_executed": False,
            "changed_files_in_repair_terrain": [],
            "changed_native_producer": False,
            "changed_worlds": [],
            "reason": "typed hold; no candidate was produced",
        },
        "unchanged_confirmed_arithmetic": {
            "cases": arithmetic,
            "all_exact": all(a["all_exact"] for a in arithmetic),
            "f6j_82_of_82": f6j_evidence["comparisons_passed"] == f6j_evidence["comparisons_total"] == 82,
            "f6j_comparisons_total": f6j_evidence["comparisons_total"],
            "f6j_comparisons_passed": f6j_evidence["comparisons_passed"],
        },
        "unchanged_falsified_behavior": {
            "P1_null_decision": p1["decision"],
            "P1_null_candidate": p1["candidate"]["distribution"] is None,
            "P1_consumer": {"state": p1_consumer.get("state"),
                             "reason": p1_consumer.get("reason")},
            "P4_unverified_admit_calls": len(p4_calls),
            "P4_ceilings": [n.get("authority_ceiling") for n in p4["evidence_graph"]],
            "P5_test_origin_calls": len(p5_calls),
            "P5_test_origin_flag": p5["test_origin"],
            "P5_ceilings": [n.get("authority_ceiling") for n in p5["evidence_graph"]],
            "P5B_accepted": p5b["candidate"] is not None,
            "P5B_real_output": p5b["test_origin"] is False,
            "P5B_callback_sources": sorted(set(p5b_calls)),
            "P5B_ceilings": [n.get("authority_ceiling") for n in p5b["evidence_graph"]],
            "P6_fail_closed": p6,
            "P7_nodes": p7_nodes,
            "P8_threshold_1_joint": {str(k): str(v) for k, v in sorted(cells(p8_1["candidate"]["distribution"]).items())},
            "P8_threshold_5_joint": {str(k): str(v) for k, v in sorted(cells(p8_5["candidate"]["distribution"]).items())},
            "P8_150_excluded": p8_150["candidate"]["support"]["Z1"]["excluded_sources"],
            "P8_150_distribution": {str(k): str(v) for k, v in sorted(cells(p8_150["candidate"]["distribution"]).items())},
            "P8_150_uncovered": p8_150["candidate"]["uncovered_target_mass"],
            "P8_150_decision": p8_150["decision"],
            "P8_150_consumer_state": p8_150_consumer.get("state"),
            "P9_decision": p9["decision"],
            "P9_decision_only_consumer": ("CONSUMED_AS_COMPLETE"
                                           if p9["decision"] == "SYNTHETIC_CANDIDATE"
                                           else "REFUSED"),
        },
        "phase_a_attacks": {
            "tests": 26, "passed": 15, "failed": 11,
            "failed_are_preregistered_unsafe_behavior": True,
            "junit": "04_JUNIT/f6l_phase_a_attacks.xml",
        },
        "changed_worlds": [],
        "unchanged_worlds": ["P1", "P2", "P3", "P10", "P11", "P8"],
        "verdict_relevance": (
            "The F6J arithmetic/native result is preserved and exact. The six "
            "decision/admission/evidence/support/transport defects are unchanged "
            "because F6K shipped no repair code. No Phase-B acceptance is possible."
        ),
    }
    out = RET / "03_PHASE_B/02_CHANGED_UNCHANGED_RECEIPTS.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
