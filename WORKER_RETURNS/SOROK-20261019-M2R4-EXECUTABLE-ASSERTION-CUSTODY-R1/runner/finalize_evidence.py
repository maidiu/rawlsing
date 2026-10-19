#!/usr/bin/env python3
"""Aggregate executed import, historical RED, proof and JUnit receipt indices."""
from __future__ import annotations

import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
E = RETURN / "evidence"
MANIFEST = RETURN / "01_SOURCE_CUSTODY_AND_IMPORT_MANIFEST.json"


def load(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xml_counts(path: Path):
    root = ET.parse(path).getroot()
    cases = list(root.iter("testcase"))
    return dict(
        tests=len(cases),
        passed=sum(1 for c in cases if c.find("failure") is None
                   and c.find("error") is None and c.find("skipped") is None),
        failed=sum(1 for c in cases if c.find("failure") is not None),
        errors=sum(1 for c in cases if c.find("error") is not None),
        skipped=sum(1 for c in cases if c.find("skipped") is not None),
        sha256=sha(path),
    )


def main() -> int:
    summary = load(E / "execution_summary.json")
    manifest = load(MANIFEST)
    imports = {}
    for path in sorted(E.glob("imported_modules_*.json")):
        variant = path.stem.replace("imported_modules_", "")
        imports[variant] = load(path)
    manifest["executed_import_receipts"] = imports
    manifest["cold_kernel_imports"] = summary["cold_imports"]
    manifest["no_change_receipt"] = summary["no_change"]
    manifest["imported_file_paths_are_return_relative"] = True
    MANIFEST.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n")

    historical = {}
    for row in summary["suites"]:
        if row["name"] in ("r3_i2_six", "r4_i2_six", "r2_child_self_control",
                           "m1_on_r2", "i2_on_r2", "m1_original", "i2_on_m1"):
            historical[row["name"]] = {
                "expected": row["expected"], "actual": row["actual"],
                "matched": row["matched"], "return_code": row["return_code"],
                "failing_nodes": row["failing_nodes"],
                "xml": row["xml"], "log": row["log"]}
    historical["accounting"] = summary["historical_accounting"]
    historical["disposition"] = (
        "Historical incompatibilities are retained as RED, not repaired or "
        "retrospectively passed. The unchanged R3-I2 two nodes fail only on R3 "
        "and pass on R4; the unchanged R2 child-self negative remains 1 PASS/1 RED.")
    (E / "historical_red_accounting.json").write_text(
        json.dumps(historical, sort_keys=True, indent=2) + "\n")

    index = {}
    for xml in sorted(E.glob("*.xml")):
        index[xml.name] = xml_counts(xml)
    (E / "junit_index.json").write_text(
        json.dumps(index, sort_keys=True, indent=2) + "\n")

    proof = dict(
        schema="SOROK_M2R4E_PROOF_WITNESS_RECEIPTS@1",
        gate_path="staged/cross_hq/proof_integrity_gate_r1.py",
        law_path="staged/cross_hq/PROOF_INTEGRITY_AND_FALSIFIABLE_TEST_LAW_R1.md",
        gate_results=summary["proof_gate"],
        kernel_restoration=summary["gate_restored_kernel"],
        lint=summary["lint"],
        claim_grades=summary["verdict_grade"],
    )
    changed_json = E / "proof_gate_changed.json"
    changed_log = E / "proof_gate_changed.log"
    if changed_json.exists():
        proof["changed_test_gate"] = {
            "receipt": changed_json.name,
            "log": changed_log.name if changed_log.exists() else None,
            "payload": load(changed_json),
        }
    (E / "proof_integrity_receipts.json").write_text(
        json.dumps(proof, sort_keys=True, indent=2) + "\n")
    print(json.dumps(dict(source_rows=len(manifest["rows"]),
                          import_variants=sorted(imports),
                          junit_files=len(index),
                          historical_controls=sorted(historical)),
                     indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
