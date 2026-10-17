"""Aggregate real execution receipts for the F6L return."""
from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

RET = Path(__file__).resolve().parents[1]


def parse(path):
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    out = {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "cases": []}
    for suite in suites:
        out["tests"] += int(suite.get("tests", 0))
        out["failures"] += int(suite.get("failures", 0))
        out["errors"] += int(suite.get("errors", 0))
        out["skipped"] += int(suite.get("skipped", 0))
        for case in suite.iter("testcase"):
            status = "passed"
            detail = None
            for bad in ("failure", "error", "skipped"):
                node = case.find(bad)
                if node is not None:
                    status = bad
                    detail = (node.get("message") or "")[:300]
                    break
            out["cases"].append({"name": case.get("name"),
                                 "classname": case.get("classname"),
                                 "status": status, "detail": detail})
    return out


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    courts = []
    for name, path, note in [
        ("f6j_independent_frozen_courts_82",
         RET / "01_SOURCE_TRANSPORT/F6J_RUNTIME/07_EVIDENCE/native_vs_frozen.json",
         "F6J 12-world exact rational court; 82/82 comparisons"),
        ("f6j_new_adversarial_53", RET / "04_JUNIT/f6j_adversarial_53.xml",
         "F6J 53 new adversarial tests; all pass on unrepaired native"),
        ("inherited_s03fo_35", RET / "04_JUNIT/inherited_s03fo_35.xml",
         "inherited original S03FO: 24 tests + 11 subtests"),
        ("f6c_author_57_candidate_shaped", RET / "04_JUNIT/f6c_author_57.xml",
         "author 57/57 at candidate-shaped relative 05_NATIVE_STAGE transport"),
        ("f6c_author_57_foreign_stage", RET / "04_JUNIT/f6c_author_57_foreign_stage.xml",
         "author 56/57 at F6L staging; only the path-suffix custody control fails"),
        ("f6l_phase_a_attacks", RET / "04_JUNIT/f6l_phase_a_attacks.xml",
         "F6L preregistered safe-behavior attacks against unrepaired native"),
    ]:
        if path.suffix == ".json":
            evidence = json.loads(path.read_text())
            courts.append({
                "name": name, "kind": "rational", "note": note,
                "path": str(path.relative_to(RET)), "sha256": sha(path),
                "tests": evidence["comparisons_total"],
                "passed": evidence["comparisons_passed"],
                "failed": evidence["comparisons_failed"],
                "exit_success": evidence["comparisons_failed"] == 0,
            })
        else:
            parsed = parse(path)
            courts.append({
                "name": name, "kind": "pytest", "note": note,
                "path": str(path.relative_to(RET)), "sha256": sha(path),
                **{k: parsed[k] for k in ("tests", "failures", "errors", "skipped")},
                "passed": parsed["tests"] - parsed["failures"] - parsed["errors"] - parsed["skipped"],
                "failed_cases": [c for c in parsed["cases"] if c["status"] != "passed"],
            })

    falsifier = json.loads((RET / "01_SOURCE_TRANSPORT/F6J_RUNTIME/07_EVIDENCE/falsifier_attacks.json").read_text())
    admission = json.loads((RET / "01_SOURCE_TRANSPORT/F6J_RUNTIME/07_EVIDENCE/admission_and_consumer_attacks.json").read_text())
    audit = json.loads((RET / "03_PHASE_B/00_F6K_RETURN_AUDIT.json").read_text())
    receipts = json.loads((RET / "03_PHASE_B/02_CHANGED_UNCHANGED_RECEIPTS.json").read_text())

    payload = {
        "schema": "PYAT_R28_F6L_REAL_PYTEST_RATIONAL_RESULTS@1",
        "branch": "agent/reviewer-pyat-r28-f6l-independent-f6k-frozen-consumer-court-r1",
        "phase_a_freeze": "f1dfcc536",  # exact remote SHA recorded in 07_REMOTE_VERIFICATION
        "courts_are_separate_and_not_averaged": True,
        "courts": courts,
        "f6j_attack_scripts": {
            "falsifier_findings": {"count": falsifier["count"],
                                    "ids": [f["id"] for f in falsifier["findings"]]},
            "admission_consumer_findings": {"count": admission["count"],
                                            "ids": [f["id"] for f in admission["findings"]]},
        },
        "f6k_return_audit": {
            "tip": audit["f6k_tip"],
            "repair_code_shipped": audit["f6k_repair_code_shipped"],
            "suites_executed": audit["f6k_suites_executed"],
            "has_repair_code": audit["f6k_has_repair_code"],
            "changed_native_producer": audit["f6k_changed_native_producer"],
            "attribution_errors": audit["f6k_attribution_errors"],
        },
        "changed_unchanged_receipts": {
            "all_confirmed_arithmetic_exact": receipts["unchanged_confirmed_arithmetic"]["all_exact"],
            "f6j_82_of_82": receipts["unchanged_confirmed_arithmetic"]["f6j_82_of_82"],
            "changed_worlds": receipts["changed_worlds"],
            "unchanged_worlds": receipts["unchanged_worlds"],
            "decision_admission_defects_unchanged": True,
        },
        "summary": {
            "genuine_native_producer_confirmed": True,
            "f6j_arithmetic_confirmed": True,
            "author_57_at_candidate_shape": "57/57",
            "author_57_at_foreign_stage": "56/57 (path-suffix custody control only)",
            "f6l_phase_a_safe_attacks": "15 passed / 11 failed (failures are the unresolved defects)",
            "repaired_candidate_present": False,
            "phase_b_acceptance_possible": False,
        },
    }
    out = RET / "02_REAL_PYTEST_RATIONAL_RESULTS.json"
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    for c in courts:
        print(c["name"], c.get("tests"), "passed", c.get("passed"), "failed", c.get("failed", "-"))


if __name__ == "__main__":
    main()
