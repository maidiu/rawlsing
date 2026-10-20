#!/usr/bin/env python3
"""Separate-process dependency-severance runner for the C9P candidate tranche.

Each named assertion runs in its own fresh Python process in the positive
baseline, then again in another fresh process with the exact dependency severed
by a source-code fault. The same named assertion must fail BY ITS OWN ASSERTION
under the fault, not by an import error, fixture crash or unrelated exception.

Usage:
    python3 severance/run_severance.py --root <repo-root> \
        --receipt evidence/severance_receipt.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

SCHEMA = "C9P_SEVERANCE_R1"

# Pre-registered named assertions and their exact source-code faults.
# Each fault severs one upstream edge of the candidate chain.
SEVERANCE_CASES: tuple[dict, ...] = (
    {
        "claim_id": "C9P_LATER_ACTION_CONSUMER_READS_COMMITTED_TARGET_STATE",
        "named_assertion": "test_later_action_consumer_reads_committed_target_state",
        "test_node": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/tests/test_severance_witnesses.py::test_later_action_consumer_reads_committed_target_state"
        ),
        "severed_edge": "committed target_state row -> LaterActionConsumer.read_target",
        "fault_path": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/candidate/later_action.py"
        ),
        "old": "record, state_hash = consumer.read_target(store, middle_state_id, as_of)",
        "new": 'record, state_hash = None, ""',
    },
    {
        "claim_id": "C9P_RESPONSE_LOOKUP_CONSUMES_EXACT_RULE_REGISTRY_ENTRY",
        "named_assertion": "test_response_lookup_consumes_exact_rule_registry_entry",
        "test_node": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/tests/test_severance_witnesses.py::test_response_lookup_consumes_exact_rule_registry_entry"
        ),
        "severed_edge": "response rule registry entry -> lookup_rule key dereference",
        "fault_path": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/candidate/response_rules.py"
        ),
        "old": "entry = registry.rules.get(key)",
        "new": "entry = None",
    },
    {
        "claim_id": "C9P_TARGET_DECISION_CONSUMES_INDEPENDENT_PERMISSION",
        "named_assertion": "test_target_decision_consumes_independent_permission",
        "test_node": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/tests/test_severance_witnesses.py::test_target_decision_consumes_independent_permission"
        ),
        "severed_edge": "separately authenticated TargetPermission -> CREATE branch",
        "fault_path": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/candidate/target_rules.py"
        ),
        "old": "if not _valid(permission):",
        "new": "if True:",
    },
    {
        "claim_id": "C9P_CONDITIONING_READSET_BINDS_PERSON_WORLD_SOURCES",
        "named_assertion": "test_conditioning_readset_binds_person_world_sources",
        "test_node": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/tests/test_severance_witnesses.py::test_conditioning_readset_binds_person_world_sources"
        ),
        "severed_edge": "person/world ConditioningSource -> readset append",
        "fault_path": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/candidate/conditioning.py"
        ),
        "old": "readset.append(source_ref)",
        "new": 'readset.append("SEVERED_SOURCE_REF")',
    },
    {
        "claim_id": "C9P_ACTION_ADMISSION_BINDS_PERFORMED_ACTION_RECEIPT",
        "named_assertion": "test_action_admission_binds_performed_action_receipt",
        "test_node": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/tests/test_severance_witnesses.py::test_action_admission_binds_performed_action_receipt"
        ),
        "severed_edge": "performed-action owner receipt -> admit_performed_action",
        "fault_path": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/candidate/action_admission.py"
        ),
        "old": "if owner_receipt is None:",
        "new": "if True:",
    },
    {
        "claim_id": "C9P_TRANSACTION_READSET_BINDS_ADMITTED_EVENT_WITNESS",
        "named_assertion": "test_transaction_readset_binds_admitted_event_witness",
        "test_node": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/tests/test_severance_witnesses.py::test_transaction_readset_binds_admitted_event_witness"
        ),
        "severed_edge": "admitted occurrence witness -> commit receipt joint identity",
        "fault_path": (
            "WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1"
            "/candidate/transaction.py"
        ),
        "old": 'joint_transaction_id=receipt["hash"],',
        "new": 'joint_transaction_id="SEVERED",',
    },
)


def _run_test(root: Path, node: str, junit: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "--junitxml",
            str(junit),
            node,
        ],
        cwd=str(root),
        text=True,
        capture_output=True,
        timeout=120,
    )


def _case_state(junit: Path, name: str) -> tuple[bool, bool, bool]:
    """Return (failed, errored, skipped) for the named test in the JUnit XML."""
    if not junit.is_file():
        return False, False, False
    tree = ET.parse(junit)
    cases = [c for c in tree.iter("testcase") if c.attrib.get("name") == name]
    if len(cases) != 1:
        return False, False, False
    case = cases[0]
    return (
        case.find("failure") is not None,
        case.find("error") is not None,
        case.find("skipped") is not None,
    )


def run_severance(root: Path) -> dict:
    """Run every pre-registered severance case in fresh separate processes."""
    root = root.resolve()
    results: list[dict] = []
    for case in SEVERANCE_CASES:
        fault_file = root / case["fault_path"]
        before = fault_file.read_text(encoding="utf-8")
        if before.count(case["old"]) != 1:
            raise RuntimeError(
                f"{case['claim_id']}: fault text is not unique in {case['fault_path']}"
            )
        named = case["named_assertion"]
        with tempfile.TemporaryDirectory(prefix="c9p-sev-") as tmp:
            tmpdir = Path(tmp)
            base_xml = tmpdir / "base.xml"
            mutant_xml = tmpdir / "mutant.xml"
            baseline = _run_test(root, case["test_node"], base_xml)
            b_fail, b_error, b_skip = _case_state(base_xml, named)
            baseline_ok = (
                baseline.returncode == 0 and not b_fail and not b_error and not b_skip
            )
            try:
                fault_file.write_text(
                    before.replace(case["old"], case["new"], 1), encoding="utf-8"
                )
                mutated = _run_test(root, case["test_node"], mutant_xml)
            finally:
                fault_file.write_text(before, encoding="utf-8")
            m_fail, m_error, m_skip = _case_state(mutant_xml, named)
            severed_red = m_fail and not m_error and not m_skip
        results.append(
            {
                "claim_id": case["claim_id"],
                "named_assertion": named,
                "severed_edge": case["severed_edge"],
                "fault_path": case["fault_path"],
                "baseline": "PASS" if baseline_ok else "BASELINE_NOT_GREEN",
                "fault_probe": (
                    "TARGET_ASSERTION_RED"
                    if severed_red
                    else (
                        "MUTANT_ERROR_NOT_ASSERTION"
                        if m_error
                        else "MUTANT_DID_NOT_RED"
                    )
                ),
                "proof_grade": (
                    "CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED"
                    if baseline_ok and severed_red
                    else "NOT_PROVED"
                ),
            }
        )
    all_proved = all(
        r["proof_grade"] == "CLAIM_EDGE_FALSIFIED_BY_CONTROL_AND_POSITIVE_SURVIVED"
        for r in results
    )
    return {
        "schema": SCHEMA,
        "status": (
            "ALL_SEVERANCE_WITNESSES_RED_SAME_NAMED_ASSERTION"
            if all_proved
            else "SEVERANCE_INCOMPLETE"
        ),
        "separate_processes": True,
        "cases": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    receipt = run_severance(args.root)
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": receipt["status"], "cases": len(receipt["cases"])}))
    if receipt["status"] != "ALL_SEVERANCE_WITNESSES_RED_SAME_NAMED_ASSERTION":
        sys.exit(1)


if __name__ == "__main__":
    main()
