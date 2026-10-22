#!/usr/bin/env python3
"""Independent R00V-R2 requalification receipts."""
from __future__ import annotations

import copy
import hashlib
import json
import platform
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = next(parent for parent in HERE.parents if (parent / ".git").exists())
RETURN = HERE.parents[1]
EVID = RETURN / "evidence"
CANDIDATE = ROOT / "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1/revisions/r2"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tests/universal_execution_oracle"))

import test_r00v_r2_requalification as T  # noqa: E402
from CROSS_HQ_CONTROL_ROOM.universal_promotion_gate import (  # noqa: E402
    DEFAULT_COMMIT, DEFAULT_ROOT, evaluate_r56_sourcefree_claim,
    load_pinned_policy,
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", *args],
                                   cwd=str(ROOT), text=True).strip()


def main():
    handle = load_pinned_policy(DEFAULT_COMMIT, DEFAULT_ROOT, "CANONICAL_V1")
    blobs, synthetic, canonical_ops = T.independent_policy()
    cases = json.loads(T.CASES_PATH.read_text())["cases"]
    results = []
    for case in cases:
        variant = (case.get("input_overlay", {})
                   .get("external_policy_resolution", {})
                   .get("variant_id", "CANONICAL_V1")) or "CANONICAL_V1"
        _, _, ops = T.independent_policy(variant)
        use_handle = handle if variant == "CANONICAL_V1" else load_pinned_policy(
            DEFAULT_COMMIT, DEFAULT_ROOT, variant)
        decision = evaluate_r56_sourcefree_claim(T.materialize(case, ops),
                                                 externally_pinned_policy=use_handle)
        expected = case["expected"]
        problems = []
        for key in ("decision", "grade_ceiling", "reason_rule_ids"):
            if decision.get(key) != expected.get(key):
                problems.append(key)
        if "expected_count" in expected and len(decision["considered_expected_ids"]) != expected["expected_count"]:
            problems.append("expected_count")
        if "expected_missing_count" in expected and len(decision["submitted_id_diff"]["missing"]) != expected["expected_missing_count"]:
            problems.append("expected_missing_count")
        if "expected_extra_count" in expected and len(decision["submitted_id_diff"]["extra"]) != expected["expected_extra_count"]:
            problems.append("expected_extra_count")
        if "expected_missing_ids" in expected and decision["submitted_id_diff"]["missing"] != expected["expected_missing_ids"]:
            problems.append("expected_missing_ids")
        if "exact_diff" in expected:
            for key in ("missing", "extra"):
                if decision["submitted_id_diff"][key] != expected["exact_diff"][key]:
                    problems.append(f"exact_diff.{key}")
        if "considered_expected_ids" in expected and decision["considered_expected_ids"] != sorted(expected["considered_expected_ids"]):
            problems.append("considered_expected_ids")
        if "materialized_variant_ref" in expected and decision.get("materialized_variant_ref") != expected["materialized_variant_ref"]:
            problems.append("materialized_variant_ref")
        results.append({"case_id": case["case_id"], "variant": variant,
                        "decision": decision["decision"],
                        "ceiling": decision["grade_ceiling"],
                        "reasons": decision["reason_rule_ids"],
                        "pass": not problems, "problems": problems})
    replay = {"schema": "R56_R00V_R2_REPLAY@1",
              "candidate": "3d4d77e9b667a1cddac07c3bfdda7d8795de458d",
              "policy_commit": DEFAULT_COMMIT, "policy_root": DEFAULT_ROOT,
              "policy_blobs_independently_recomputed": blobs,
              "expected_count": len(canonical_ops),
              "case_count": len(results),
              "passed": sum(1 for row in results if row["pass"]),
              "all_pass": all(row["pass"] for row in results),
              "results": results}
    (EVID / "reviewer_replay.json").write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf8")

    baseline = T.baseline_claim()
    probes = []
    def probe(name, claim, secure):
        decision = evaluate_r56_sourcefree_claim(claim, externally_pinned_policy=handle)
        probes.append({"name": name, "actual": decision["decision"],
                       "reasons": decision["reason_rule_ids"],
                       "expected_secure": sorted(secure),
                       "pass": decision["decision"] in secure})
    c = copy.deepcopy(baseline); c["request"]["claim_kind"] = "EXECUTED_NATIVE"
    probe("executed_native_without_evidence", c, {"HOLD_TRUSTED_NATIVE", "REFUSE_FORGED_EVIDENCE", "REFUSE_AUTHORITY"})
    c = copy.deepcopy(baseline); op = c["submitted"]["operation_objects"][0]
    c["submitted"]["operation_status_edits"] = [{"operation_id": op["operation_id"], "execution": "COMPLETED", "result": "SUPPORTED", "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    probe("supported_status_without_native_evidence", c, {"HOLD_TRUSTED_NATIVE", "REFUSE_STATUS", "REFUSE_FORGED_EVIDENCE"})
    c = copy.deepcopy(baseline)
    prohibited = next(r for r in canonical_ops if r.get("axis_bindings", {}).get("eligibility") == "PROHIBITED")
    c["submitted"]["operation_status_edits"] = [{"operation_id": prohibited["operation_id"], "eligibility": "ELIGIBLE", "execution": "COMPLETED", "result": "OBSERVED_ZERO", "denominator": {"t": "integer", "v": "8"}, "numerator": {"t": "integer", "v": "0"}, "proof_source": "TEST_ONLY_HAND_DERIVED"}]
    probe("prohibited_completed_observed_zero", c, {"REFUSE_STATUS"})
    c = copy.deepcopy(baseline); c["submitted"]["operation_objects"][0]["direction_ref"] = "TEST:CHANGED"
    c["submitted"]["operation_status_edits"] = [{"operation_id": c["submitted"]["operation_objects"][0]["operation_id"], "execution": "NOT_STARTED", "result": "UNKNOWN"}]
    probe("semantic_mutation_masked_by_status_edit", c, {"REFUSE_FRONTIER"})
    c = copy.deepcopy(baseline); c["request"]["claim_grade"] = "MADE_UP"
    probe("unknown_claim_grade", c, {"REFUSE_AUTHORITY", "REFUSE_STATUS", "REFUSE_PIN"})
    c = copy.deepcopy(baseline); c["submitted"]["occurrence_objects"] = [
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET", "administration": "ADMINISTERED"},
        {"occurrence_ref": "x", "item": "lumen", "role": "TARGET", "administration": "ADMINISTERED"}]
    probe("duplicate_occurrence_objects", c, {"REFUSE_FRONTIER"})
    bad = T.dataclasses.replace(handle, policy=dict(handle.policy, contract_id="OTHER"))
    d = evaluate_r56_sourcefree_claim(baseline, externally_pinned_policy=bad)
    probes.append({"name": "policy_contract_mismatch", "actual": d["decision"],
                   "reasons": d["reason_rule_ids"],
                   "expected_secure": ["REFUSE_IDENTITY", "REFUSE_PIN"],
                   "pass": d["decision"] in {"REFUSE_IDENTITY", "REFUSE_PIN"}})
    c = copy.deepcopy(baseline)
    eligible = next(r for r in canonical_ops if r.get("axis_bindings", {}).get("eligibility") == "ELIGIBLE")
    c["submitted"]["operation_disposition_edits"] = [{"operation_id": eligible["operation_id"], "to": "HELD"}]
    probe("eligible_to_held_disposition", c, {"REFUSE_STATUS"})
    defects = {"schema": "R56_R00V_R2_DEFECT_REQUALIFICATION@1",
               "source_review": "140c41d6a10a595ff5d80de4eb855bcd65e7a8f6",
               "candidate": "3d4d77e9b667a1cddac07c3bfdda7d8795de458d",
               "probes": probes, "defect_count": len(probes),
               "passed": sum(1 for row in probes if row["pass"]),
               "all_repaired": all(row["pass"] for row in probes)}
    (EVID / "defect_requalification.json").write_text(json.dumps(defects, indent=2, sort_keys=True) + "\n", encoding="utf8")

    manifest = json.loads((CANDIDATE / "manifest.json").read_text())
    bad_files = []
    for row in manifest["files"]:
        path = ROOT / row["path"]
        if not path.exists() or sha(path) != row["sha256"]:
            bad_files.append({"path": row["path"], "recorded": row["sha256"],
                              "actual": sha(path) if path.exists() else "MISSING"})
    sums = []
    for line in (CANDIDATE / "evidence/SHA256SUMS.txt").read_text().splitlines():
        if not line.strip():
            continue
        digest, path = line.split("  ", 1)
        resolved = None
        for base in (CANDIDATE, CANDIDATE / "evidence", ROOT):
            candidate_path = (base / path).resolve()
            if candidate_path.exists():
                resolved = candidate_path
                break
        sums.append({"path": path, "recorded": digest,
                     "resolved": str(resolved.relative_to(ROOT)) if resolved else "",
                     "actual": sha(resolved) if resolved else "",
                     "pass": bool(resolved and sha(resolved) == digest)})
    custody = {"schema": "R56_R00V_R2_CANDIDATE_CUSTODY@1",
               "manifest_files": len(manifest["files"]),
               "manifest_bad": bad_files,
               "manifest_all_hashes_match": not bad_files,
               "sums_entries": len(sums),
               "sums_bad": [row for row in sums if not row["pass"]],
               "sums_all_resolve": all(row["pass"] for row in sums),
               "note": "Candidate manifest self-excludes itself and sums; checks are against actual candidate files."}
    (EVID / "candidate_custody_recheck.json").write_text(json.dumps(custody, indent=2, sort_keys=True) + "\n", encoding="utf8")

    junit = {}
    junit_path = EVID / "junit/r00v_r2.xml"
    if junit_path.exists():
        suite = ET.parse(junit_path).getroot().find("testsuite")
        junit = {k: suite.attrib[k] for k in ("tests", "failures", "errors", "skipped", "time")}
    passport = {"schema": "R56_R00V_R2_PASSPORT@1",
                "model_declared": "DeepSeek V4.1-Flash", "reasoning_declared": "MAX",
                "intelligence": "I2-I3", "execution": "S3 local Git/Python/pytest",
                "harness": "OpenCode local session", "host": platform.platform(),
                "machine": platform.machine(), "python": sys.version.split()[0],
                "git": git("--version"), "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
                "head_at_evidence_time": git("rev-parse", "HEAD"),
                "candidate": "3d4d77e9b667a1cddac07c3bfdda7d8795de458d",
                "policy_commit": DEFAULT_COMMIT,
                "shared_native": "eb28fdcc311e2534b66def445e745cb25cb8a9bd",
                "shared_review": "485f31e52ca82905dcfbbc79c5f8c8294fb55f49",
                "r57": "953eb07ad29cc424b2fc43cfeb13ef83355f3a50",
                "external_model_calls": 0, "usage": "UNKNOWN", "cost": "UNKNOWN",
                "r09": "NOT_GRANTED", "original": "UNISSUED", "junit": junit}
    (EVID / "passport.json").write_text(json.dumps(passport, indent=2, sort_keys=True) + "\n", encoding="utf8")
    witness = {"schema": "R56_R00V_R2_PROOF_WITNESS@1",
               "candidate_gate_sha256": sha(ROOT / "CROSS_HQ_CONTROL_ROOM/universal_promotion_gate.py"),
               "reviewer_test_sha256": sha(ROOT / "tests/universal_execution_oracle/test_r00v_r2_requalification.py"),
               "replay_sha256": sha(EVID / "reviewer_replay.json"),
               "defect_sha256": sha(EVID / "defect_requalification.json"),
               "junit_sha256": sha(EVID / "junit/r00v_r2.xml"),
               "commands": {"tests": "PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -m pytest tests/universal_execution_oracle -q --junitxml=WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/evidence/junit/r00v_r2.xml",
                            "replay": "PYTHONPATH=. python3 WORKER_RETURNS/PYAT-R56-R00V-INDEPENDENT-NATIVE-REVIEW-R1/revisions/r2/tools/requalify.py",
                            "dependency": "python3 tests/universal_execution_oracle/r00v_r2_dependency_probe.py {baseline,fault,restore}"},
               "cases": 36, "cases_passed": replay["passed"],
               "defects": 8, "defects_repaired": defects["passed"],
               "test_count": junit.get("tests"), "native_provenance": "NOT_PRESENT",
               "actual_consumer_values_read": None, "original_grant": "UNISSUED"}
    (EVID / "proof_witness.json").write_text(json.dumps(witness, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps({"cases": replay["passed"], "defects": defects["passed"],
                      "custody_manifest_bad": len(bad_files),
                      "custody_sums_bad": len(custody["sums_bad"]),
                      "junit": junit}, indent=1))


if __name__ == "__main__":
    main()
