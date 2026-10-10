#!/usr/bin/env python3
"""Documentary no-source-read validator for Pyat all35 completion inventory.

Usage (from repository root):
    python3 PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/validate_completion_inventory.py
Checks inventory structure, never loads SAV/DTA, never invokes pipeline runtime.
Does NOT claim source authority, empirical coverage or F1-F8 acceptance.
"""
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOM = HERE.parent

def load(filename):
    return json.loads((HERE / filename).read_text(encoding="utf-8"))

def fail(condition, message):
    if not condition:
        raise AssertionError(message)

def main():
    estate = load("ESTATE_35X_REQUIREMENTS_MATRIX.json")
    tasks = load("TASK_LEDGER_101_MACHINE.json")
    wave = load("WAVE35_COMMON_EDGE_ACTION_QUEUE.json")
    ids = [f"SRC{i:02d}" for i in range(1, 36)]
    original = estate["sources"]
    found = [r["id"] for r in original]
    fail(len(found) == len(set(found)) == len(ids) and found == ids,
         "35 source identities missing, extra, duplicate or wrong order")
    fail(estate["source_count"] == 35, "source_count")
    native = [x["id"] for x in estate["axes_source_native"]]
    ee = estate["axes_EE01_EE16"]
    fs = [x["id"] for x in estate["axes_F1_F8"]]
    fail(native == [f"S{i:02d}" for i in range(1, 31)], "30 source-native obligations")
    fail(ee == [f"EE{i:02d}" for i in range(1, 17)], "EE01-EE16")
    fail(fs == [f"F{i}" for i in range(1, 9)], "F1-F8")
    fail(estate["expected_source_axis_cells"] == 1050, "native cell count")
    fail(estate["expected_ee_axis_cells"] == 560, "EE cell count")
    fail(estate["expected_f_axis_cells"] == 280, "F cell count")
    for src in original:
        fail(src["established_membership"] == "GOVERNED_CLOSED35__MANDATORY_ACCOUNTING",
             f"{src['id']}: lost mandatory source membership")
        fail(src.get("no_drop_assertion") is True, f"{src['id']}: missing no-drop assertion")
        fail([x["id"] for x in src["source_native_axes"]] == native,
             f"{src['id']}: native axes mismatch")
        fail([x["id"] for x in src["empirical_engine_axes"]] == ee,
             f"{src['id']}: EE axes mismatch")
        fail([x["id"] for x in src["f1_f8_axes"]] == fs,
             f"{src['id']}: F axes mismatch")
        fail(bool(src.get("original_dossier")), f"{src['id']}: missing original dossier ref")
        fail(src["historical_representation_census"].startswith("HISTORICAL_"),
             f"{src['id']}: historical representation improperly made current")
        for x in src["source_native_axes"]:
            if x["status"] == "SOURCE_INTRINSIC_NONAPPLICABILITY_PROVED":
                fail(bool(x.get("nonapplicability_original_source_evidence_ref")),
                     f"{src['id']} {x['id']}: nonapplicability without original proof")
        for x in src["f1_f8_axes"]:
            if x["status"] == "ACTUAL_F_FUNCTION_CONSUMED":
                fail(bool(x.get("consumer_proof")), f"{src['id']} {x['id']}: consumerless F green")
    fail(tasks["task_count"] == len(tasks["task_rows"]) == 101, "101 work classes")
    work_ids = [x["id"] for x in tasks["task_rows"]]
    fail(len(work_ids) == len(set(work_ids)), "duplicate work class ID")
    work_md = (HERE / "GLOBAL_WORK_REGISTER.md").read_text(encoding="utf-8")
    md_ids = re.findall(r"^- ([GSPQLFTWA][0-9]{2})\.", work_md, re.M)
    fail(md_ids == work_ids, "markdown task IDs and typed task ledger disagree")
    for task in tasks["task_rows"]:
        fail(bool(task["owner_family"]) and task["existing_owner_candidate_paths"],
             f"{task['id']}: missing candidate owner family/implementation paths")
        fail(task["reconciliation_state"] != "MISSING_IMPLEMENTATION_PROVED",
             f"{task['id']}: inferred missing code without evidence")
        if task["reconciliation_state"] in ("CURRENT_ACCEPTED_AT_EXACT_SCOPE", "ACTUAL_CONSUMER_POSITIVE_PROVED"):
            fail(bool(task["current_accepted_positive_receipt"]),
                 f"{task['id']}: premature work closure without adopted positive receipt")
    fail([x["id"] for x in wave["sources"]] == ids, "35-wave edge queue mismatch")
    for src in wave["sources"]:
        fail(src["attributed_edge_classes"], f"{src['id']}: no historic edge-class accounting")
        fail(src["current_source_backed_all_expected_products_manifest_ref"] is None or
             bool(src["final_consumer_receipt_ref"]),
             f"{src['id']}: all-product claim without final consumer trace")
    readfirst = (ROOM / "00_READ_ME_FIRST.md").read_text(encoding="utf-8")
    protocol = (ROOM / "13_FRESH_HQ_FULL_GROK_PROTOCOL.md").read_text(encoding="utf-8")
    fail("00_WHOLE_MACHINE_AUTOMATION_DOCTRINE_R1.md" in readfirst[:2500],
         "read-first doctrine not prominently pinned")
    fail("00_WHOLE_MACHINE_AUTOMATION_DOCTRINE_R1.md" in protocol[:1600],
         "fresh-HQ grok doctrine not pinned")
    grok = (HERE / "ACCEPTANCE_AND_GROK_TEST.md").read_text(encoding="utf-8")
    for k in range(1,36):
        fail(f"AT{k:02d}" in grok, f"missing independent Astra AT{k:02d} in acceptance")
    print(json.dumps({
        "result": "PASS_INVENTORY_STRUCTURE_ONLY",
        "source_waves": len(found),
        "source_native_axes": len(native),
        "empirical_engine_axes": len(ee),
        "F1_F8_axes": len(fs),
        "explicit_wave_scope_cells": len(found) * (len(native) + len(ee) + len(fs)),
        "typed_global_task_classes": len(work_ids),
        "wave_edge_queue_rows": len(wave["sources"]),
        "empirical_source_rows_read": 0,
        "pipeline_executed": False,
        "F1_F8_acceptance_certified": False,
        "warning": "Passing this structural validator is never an original-item inventory, source permission, current code positive, consumer occupancy or PREV3-completion certificate."
    }, indent=2))
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (KeyError, ValueError, AssertionError) as exc:
        sys.stderr.write(f"FAIL_COMPLETION_INVENTORY: {exc}\n")
        sys.exit(1)
