#!/usr/bin/env python3
"""Execute the full M2R4 independent executable custody court and write receipts."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
RUNS = RETURN / "runs"
EVIDENCE = RETURN / "evidence"
GATE = RETURN / "staged" / "cross_hq" / "proof_integrity_gate_r1.py"
MANIFEST = RETURN / "01_SOURCE_CUSTODY_AND_IMPORT_MANIFEST.json"
EXPECTED = {row["path"]: row["sha256"] for row in
            json.loads(MANIFEST.read_text())["rows"]}

R4_GREEN = "r4_green"
R3_RED = "r3_red"
R3_NEW = "r3_new"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_pytest(name: str, run_dir: str, files: list[str], *, extra_env=None):
    run = RUNS / run_dir
    xml = EVIDENCE / (name + ".xml")
    log = EVIDENCE / (name + ".log")
    env = dict(os.environ)
    env.update({"PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"})
    env["PYTHONPATH"] = "."
    if extra_env:
        env.update(extra_env)
    command = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
               "--import-mode=importlib", *files, "--junitxml", str(xml)]
    with log.open("wb") as handle:
        result = subprocess.run(command, cwd=run, env=env, stdout=handle,
                                stderr=subprocess.STDOUT)
    return dict(name=name, run_dir=run_dir, files=files, command=command,
                return_code=result.returncode, xml=xml.name, log=log.name)


def parse_xml(path: Path):
    root = ET.parse(path).getroot()
    cases = list(root.iter("testcase"))
    rows = []
    for case in cases:
        status = "PASS"
        if case.find("failure") is not None:
            status = "FAIL"
        elif case.find("error") is not None:
            status = "ERROR"
        elif case.find("skipped") is not None:
            status = "SKIP"
        rows.append(dict(file=case.attrib.get("file", ""),
                         name=case.attrib.get("name", ""), status=status))
    return dict(tests=len(rows),
                passed=sum(x["status"] == "PASS" for x in rows),
                failed=sum(x["status"] == "FAIL" for x in rows),
                errors=sum(x["status"] == "ERROR" for x in rows),
                skipped=sum(x["status"] == "SKIP" for x in rows),
                failing=[x for x in rows if x["status"] != "PASS"],
                rows=rows)


def write_json(path: Path, payload):
    path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n")


def main() -> int:
    EVIDENCE.mkdir(exist_ok=True)
    (RUNS / "_prepared_manifest.json").exists() or subprocess.run(
        [sys.executable, str(RETURN / "runner" / "prepare_runs.py")], check=True)

    suite_specs = []
    # Historical contrast: exact unchanged R3-I2 six on R3 and R4.
    suite_specs.append(("r3_i2_six", R3_RED, ["test_fresh_i2_adversarial.py"], 6, 4, 2))
    suite_specs.append(("r4_i2_six", R4_GREEN, ["test_fresh_i2_adversarial.py"], 6, 6, 0))
    # Full inherited author suite, individually and combined.
    author_files = [
        "test_m2.py", "test_m3_independent.py", "test_m3_unresolved.py",
        "test_source_preimages.py", "test_original_preimage.py",
        "test_local_hostile.py", "test_relation_custody.py",
        "test_heldout_actor_independence.py", "test_r3_counterpart_actor_custody.py",
        "test_fresh_i2_adversarial.py", "test_r4_owner_rule_hostile.py"]
    per_suite = [
        ("r4_M2_41", ["test_m2.py"], 41),
        ("r4_M3_lawful_32", ["test_m3_independent.py"], 32),
        ("r4_M3_packaged_3", ["test_m3_unresolved.py"], 3),
        ("r4_source_preimage_15", ["test_source_preimages.py"], 15),
        ("r4_M3_historical_3", ["test_original_preimage.py"], 3),
        ("r4_old_hostile_11", ["test_local_hostile.py"], 11),
        ("r4_R2_relation_14", ["test_relation_custody.py"], 14),
        ("r4_R2_I2_heldout_2", ["test_heldout_actor_independence.py"], 2),
        ("r4_R3_owner_14", ["test_r3_counterpart_actor_custody.py"], 14),
        ("r4_fresh_I2_6", ["test_fresh_i2_adversarial.py"], 6),
        ("r4_new_12", ["test_r4_owner_rule_hostile.py"], 12),
    ]
    for name, files, count in per_suite:
        suite_specs.append((name, R4_GREEN, files, count, count, 0))
    suite_specs.append(("r4_author_153_all", R4_GREEN, author_files, 153, 153, 0))
    # Independent twelve and R3 discrimination contrast.
    suite_specs.append(("r4_i2_new_12", R4_GREEN, ["test_r4_i2_new_hostiles.py"], 12, 12, 0))
    suite_specs.append(("r3_i2_new_12_contrast", R3_NEW, ["test_r4_i2_new_hostiles.py"], 12, 6, 6))
    # Original R2 negative control and historical incompatibilities.
    suite_specs.append(("r2_child_self_control", "r2_control",
                        ["test_heldout_actor_independence.py"], 2, 1, 1))
    suite_specs.append(("m1_on_r2", "m1_on_r2", ["test_kernel.py"], 37, 18, 19))
    suite_specs.append(("i2_on_r2", "i2_on_r2", ["test_i2_strict.py"], 23, 13, 10))
    suite_specs.append(("m1_original", "m1_original", ["test_kernel.py"], 37, 37, 0))
    suite_specs.append(("i2_on_m1", "i2_on_m1", ["test_i2_strict.py"], 23, 14, 9))

    results = []
    all_expected = True
    for name, run_dir, files, tests, passed, failed in suite_specs:
        run = run_pytest(name, run_dir, files)
        parsed = parse_xml(EVIDENCE / run["xml"])
        matched = (parsed["tests"] == tests and parsed["passed"] == passed and
                   parsed["failed"] == failed and parsed["errors"] == 0 and
                   parsed["skipped"] == 0)
        all_expected &= matched
        results.append(dict(
            name=name, run_dir=run_dir, files=files, return_code=run["return_code"],
            expected=dict(tests=tests, passed=passed, failed=failed),
            actual={k: parsed[k] for k in ("tests", "passed", "failed", "errors", "skipped")},
            matched=matched, failing_nodes=[f"{x['file']}::{x['name']}"
                                            for x in parsed["failing"]],
            xml=run["xml"], log=run["log"]))

    # Cold replay of the full 153 suite in two separate processes.
    cold = []
    for label in ("cold_a", "cold_b"):
        run = run_pytest("r4_author_153_" + label, R4_GREEN, author_files)
        parsed = parse_xml(EVIDENCE / run["xml"])
        cold.append(dict(label=label, return_code=run["return_code"],
                         actual={k: parsed[k] for k in ("tests", "passed", "failed", "errors", "skipped")},
                         xml=run["xml"], log=run["log"]))
    cold_outcomes_equal = ([x["actual"]["tests"] for x in cold] == [153, 153] and
                           [x["actual"]["failed"] for x in cold] == [0, 0])

    # Claim-specific proof gate witnesses.
    gate_results = []
    for contract, label in (
            ("test_fresh_i2_adversarial.py.proof.json", "rule_binding"),
            ("test_r4_i2_new_hostiles.py.proof.json", "witness_channels")):
        receipt = EVIDENCE / ("proof_gate_" + label + "_receipt.json")
        log = EVIDENCE / ("proof_gate_" + label + ".log")
        command = [sys.executable, "-B", str(GATE), "witness",
                   str(RUNS / R4_GREEN / contract), "--root",
                   str(RUNS / R4_GREEN), "--receipt", str(receipt)]
        with log.open("wb") as handle:
            proc = subprocess.run(command, stdout=handle, stderr=subprocess.STDOUT)
        gate_results.append(dict(label=label, contract=contract, return_code=proc.returncode,
                                 receipt=receipt.name if receipt.exists() else None,
                                 log=log.name,
                                 receipt_payload=json.loads(receipt.read_text())
                                 if receipt.exists() else None))
    kernel_after = sha(RUNS / R4_GREEN / "kernel.py")
    kernel_expected = EXPECTED["staged/kernels/r4_kernel.py"]
    gate_restored = kernel_after == kernel_expected

    # Lint the newly authored test and the staged gate test.
    lint = []
    for rel in ("staged/tests/test_r4_i2_new_hostiles.py",
                "staged/cross_hq/test_proof_integrity_gate_r1.py"):
        command = [sys.executable, "-B", str(GATE), "lint", rel]
        proc = subprocess.run(command, capture_output=True, text=True, cwd=RETURN)
        lint.append(dict(file=rel, return_code=proc.returncode,
                         stdout=proc.stdout.strip(), stderr=proc.stderr.strip()))

    # Fresh-process imports and the no-change receipt.
    cold_imports = []
    for run_dir in ("r2_control", "r3_red", "r4_green"):
        command = [sys.executable, "-B", str(RETURN / "runner" / "cold_import.py"),
                   str(RUNS / run_dir), str(RETURN)]
        proc = subprocess.run(command, capture_output=True, text=True, cwd=RUNS / run_dir)
        payload = json.loads(proc.stdout) if proc.returncode == 0 else {"error": proc.stderr}
        cold_imports.append(payload)
    no_change = subprocess.run(
        [sys.executable, "-B", str(RETURN / "runner" / "no_change_receipt.py"),
         str(RUNS / R4_GREEN), str(RETURN)], capture_output=True, text=True,
        cwd=RUNS / R4_GREEN)
    no_change_payload = json.loads(no_change.stdout) if no_change.returncode == 0 else {
        "error": no_change.stderr}

    # Sanitize hostnames and host paths in evidence text.
    replacements = 0
    for path in EVIDENCE.iterdir():
        if path.suffix not in (".xml", ".log", ".json"):
            continue
        text = path.read_text(errors="replace")
        new = re.sub(r'hostname="[^"]*"', 'hostname="sanitized-host"', text)
        new = re.sub("/" + "Users/[^ \n:\"']+", "<sanitized-host-path>", new)
        new = new.replace(str(RETURN), "<return-root>").replace(str(RUNS), "<runs>")
        if new != text:
            path.write_text(new)
            replacements += 1

    summary = dict(
        schema="SOROK_M2R4E_EXECUTION_SUMMARY@1",
        environment=dict(python=sys.version.split()[0], pytest=subprocess.check_output(
            [sys.executable, "-m", "pytest", "--version"], text=True).strip()),
        suites=results,
        all_expected_outcomes=all_expected,
        cold_full_153=cold,
        cold_outcomes_equal=cold_outcomes_equal,
        proof_gate=gate_results,
        gate_restored_kernel=dict(actual=kernel_after, expected=kernel_expected,
                                  match=gate_restored),
        lint=lint,
        cold_imports=cold_imports,
        no_change=no_change_payload,
        evidence_sanitized_files=replacements,
        historical_accounting=dict(
            m1_on_r2="19 RED / 18 PASS retained", i2_on_r2="10 RED / 13 PASS retained",
            m1_original="37 PASS", i2_on_m1="9 RED / 14 PASS retained",
            original_R2_child_self="1 PASS / 1 RED retained"),
        verdict_grade=dict(
            EXECUTED_GREEN=all_expected,
            ASSERTION_EFFICACY_PROVED=(all(x["return_code"] == 0 for x in gate_results)
                                       and gate_restored),
            CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED=(
                all(x["return_code"] == 0 for x in gate_results) and gate_restored),
            SCIENCE="bounded sourcefree executable custody court only",
        ),
    )
    write_json(EVIDENCE / "execution_summary.json", summary)
    print(json.dumps(dict(all_expected=all_expected, cold_equal=cold_outcomes_equal,
                          gate_ok=all(x["return_code"] == 0 for x in gate_results),
                          gate_restored=gate_restored, suites=len(results)),
                     indent=2))
    return 0 if (all_expected and cold_outcomes_equal and gate_restored and
                 all(x["return_code"] == 0 for x in gate_results)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
