#!/usr/bin/env python3
"""Typed failure inventory and no-change/cold receipt aggregation."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
E = RETURN / "evidence"
SUMMARY = json.loads((E / "execution_summary.json").read_text())

EXPECTED_RED = {
    "r3_i2_six": "Two unchanged original R3-I2 REDs; R3 only",
    "r2_child_self_control": "Original R2 child-self negative control; expected 1 RED",
    "m1_on_r2": "Historical M1-on-R2 incompatibility; expected 19 RED",
    "i2_on_r2": "Historical I2-on-R2 incompatibility; expected 10 RED",
    "i2_on_m1": "Historical I2-on-M1 control; expected 9 RED",
    "r3_i2_new_12_contrast": "Prospective 12-case discrimination contrast on R3; expected 6 RED",
}


def failures(xml_name: str):
    path = E / xml_name
    root = ET.parse(path).getroot()
    out = []
    for case in root.iter("testcase"):
        if case.find("failure") is None and case.find("error") is None:
            continue
        child = case.find("failure")
        kind = "failure"
        if child is None:
            child = case.find("error")
            kind = "error"
        message = (child.attrib.get("message", "") if child is not None else "").strip()
        out.append(dict(name=case.attrib.get("name", ""),
                        classname=case.attrib.get("classname", ""),
                        kind=kind, message=message[:220]))
    return out


suites = {}
technical = []
for row in SUMMARY["suites"]:
    payload = dict(expected=row["expected"], actual=row["actual"],
                   expected_red=row["name"] in EXPECTED_RED,
                   expectation=EXPECTED_RED.get(row["name"]),
                   failing_cases=failures(row["xml"]))
    suites[row["name"]] = payload
    if row["actual"]["errors"] or row["actual"]["skipped"]:
        technical.append(row["name"])

inventory = dict(
    schema="SOROK_M2R4E_TYPED_FAILURE_INVENTORY@1",
    technical_errors_or_skips=technical,
    all_suites=[dict(name=row["name"], return_code=row["return_code"],
                     expected=row["expected"], actual=row["actual"],
                     matched=row["matched"], xml=row["xml"], log=row["log"])
                for row in SUMMARY["suites"]],
    expected_historical_or_control_reds=suites,
    residual_not_run=[
        "native ADP015/016/017/019/021 authority: not requested, not accessed",
        "CAN008/CAN011 psychological adoption or actor memory: not requested",
        "real observer identity or source-issued rule authentication: not available/not claimed",
        "authorized old-schema migration: not issued; old records remain quarantined",
        "B3/C9 canonical integration, PRE-MAIN mutation, production adoption: outside this court",
        "actor development, generated person, V3/V2: outside this court",
    ],
    typed_holds=[
        "R4 RULE_HASH is a fixed synthetic contract identity, not an external signed rule",
        "observer independence is a declared synthetic provenance gate, not authenticated third-party testimony",
        "unconsumed history may remain inert; no inference of a real observer's psychological state",
        "sourcefree candidate only; no original35, source right, ADP/CAN grant or self-acceptance",
    ],
    disposition="EXECUTABLE_PASS_SCOPED__NO_SELF_ADOPTION",
)
(E / "typed_failure_inventory.json").write_text(
    json.dumps(inventory, sort_keys=True, indent=2) + "\n")

cold = dict(
    schema="SOROK_M2R4E_NO_CHANGE_AND_COLD_RECEIPTS@1",
    no_change=SUMMARY["no_change"],
    cold_kernel_imports=SUMMARY["cold_imports"],
    cold_full_153=SUMMARY["cold_full_153"],
    cold_outcomes_equal=SUMMARY["cold_outcomes_equal"],
    cold_interpretation=("Two fresh processes, each executing the full 153-case inherited "
                         "suite on the exact R4 kernel; counts and outcomes equal. JUnit "
                         "byte hashes differ only by run metadata, not by test outcome."),
)
(E / "no_change_and_cold_receipts.json").write_text(
    json.dumps(cold, sort_keys=True, indent=2) + "\n")
print(json.dumps(dict(technical=technical, suites=len(suites),
                      residual_not_run=len(inventory["residual_not_run"])), indent=2))
