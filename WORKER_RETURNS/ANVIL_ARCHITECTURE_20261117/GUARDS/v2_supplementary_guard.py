#!/usr/bin/env python3
"""Supplementary v2 guard for the ANVIL architecture candidate.

Calls the accepted instrument DECISION guard, then checks the four v2
addendum requirements, their dispositions/crosswalk rows, the received
specialist state, and the selected/conditional/held design coherence.

This does not modify or fork the accepted instrument. A local PASS is
structural only: not independent C, native/source/science proof or H1.
"""
from __future__ import annotations
import argparse, json, pathlib, subprocess, sys

V2_IDS = (
    "REQ-COST-LAYER-DECOMPOSITION",
    "REQ-DERIVED-INDEX-BINDING",
    "REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY",
    "REQ-CONSTRUCTION-ATOMIC-RECOVERY",
)
BASE_IDS = (
    "REQ-SOURCE-SEMANTICS","REQ-C11-PERSISTENCE","REQ-CURRENT-I03-I05",
    "REQ-HISTORICAL-DDM","REQ-F1-F4","REQ-FIELD-FORGE","REQ-SEAM-WORLD-ACTOR",
    "REQ-AUTHORITY-RECOVERY","REQ-RESOURCE-ECONOMICS","REQ-MULTIWAY-JOINT",
    "REQ-DENOMINATOR-MISSING-ROUTING","REQ-PHYSICAL-WORKLOAD-1-10-100",
    "REQ-SOURCE-I02-REVOCATION","REQ-FF01-FF02-WORLD-ACTOR-FIREWALL",
    "REQ-TERMINAL-F5-F8-N11-N12","REQ-HISTORICAL-NOADOPTION-CONSERVATION",
)
FORBIDDEN_EFFECTS = (
    "SC-ESTATE removes",
    "durable index and prepared session target",
    "The index is bound",
)


def fail(errors, code):
    errors.append(code)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--decision", required=True)
    ap.add_argument("--addendum", required=True)
    ap.add_argument("--crosswalk", required=True)
    ap.add_argument("--evidence-root", required=True)
    ap.add_argument("--source-root", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--zip", required=True)
    ap.add_argument("--accepted-guard", default="/Users/matthewsmith/Desktop/ANVIL_ARCHITECTURE_EXECUTION_20261117/ACCEPTED_INSTRUMENT/ANVIL_R7/tools/r7_integrated.py")
    ap.add_argument("--skip-accepted", action="store_true")
    a = ap.parse_args()
    errors = []
    decision = json.loads(pathlib.Path(a.decision).read_text())
    addendum = json.loads(pathlib.Path(a.addendum).read_text())
    crosswalk = pathlib.Path(a.crosswalk).read_text().splitlines()

    accepted = None
    if not a.skip_accepted:
        cmd = [sys.executable, a.accepted_guard, "DECISION", a.decision,
               "--evidence-root", a.evidence_root, "--source-root", a.source_root,
               "--repo", a.repo, "--zip", a.zip]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        try:
            accepted = json.loads(proc.stdout)
        except Exception:
            accepted = {"status": "UNPARSEABLE", "stdout": proc.stdout, "stderr": proc.stderr}
        if proc.returncode != 0 or accepted.get("status") != "PASS_LOCAL_INTEGRATED_DECISION_PENDING_C":
            fail(errors, "ACCEPTED_GUARD_NOT_PASS")
        if accepted.get("covered") != 16 or accepted.get("identity_dispositions") != 118:
            fail(errors, "ACCEPTED_GUARD_BASELINE_COUNTS")

    # v2 addendum and decision linkage
    reqs = addendum.get("new_requirements")
    if not isinstance(reqs, list) or len(reqs) != 4:
        fail(errors, "V2_ADDENDUM_NOT_FOUR")
        req_ids = []
    else:
        req_ids = [r.get("id") for r in reqs]
        if tuple(req_ids) != V2_IDS:
            fail(errors, "V2_ADDENDUM_IDS_DRIFT")
    for r in reqs or []:
        if r.get("binding") not in ("PRESENT_HARD", "FUTURE_NONPRECLUSION", "EXTERNAL_OWNER_HELD"):
            fail(errors, "V2_BAD_BINDING:" + str(r.get("id")))
        for k in ("substantive_requirement","why_needed","positive_probe","negative_probe","architectural_consequence"):
            if not isinstance(r.get(k), str) or len(r[k].strip()) < 25:
                fail(errors, "V2_VACUOUS:" + str(r.get("id")) + ":" + k)
    fv = decision.get("frame_v2_addendum") or {}
    if fv.get("path") != "S1/FRAME_V2_ADDENDUM.json":
        fail(errors, "V2_DECISION_PATH")
    if fv.get("sha256") != __import__("hashlib").sha256(pathlib.Path(a.addendum).read_bytes()).hexdigest():
        fail(errors, "V2_DECISION_SHA")
    if tuple(fv.get("new_requirement_ids") or ()) != V2_IDS:
        fail(errors, "V2_DECISION_IDS")

    # dispositions
    disp = decision.get("candidate_requirement_addendum_dispositions")
    if not isinstance(disp, list) or len(disp) != 4:
        fail(errors, "V2_DISPOSITIONS_NOT_FOUR")
        disp_ids = []
    else:
        disp_ids = [x.get("requirement_id") for x in disp]
        if tuple(disp_ids) != V2_IDS:
            fail(errors, "V2_DISPOSITION_IDS")
        for x in disp:
            if x.get("disposition") not in ("PRESENT_PRESERVED","FUTURE_NONPRECLUDED","EXACT_OWNER_HOLD","BLOCKING_LOSS","REFUSED_AUTHORITY"):
                fail(errors, "V2_BAD_DISPOSITION:" + str(x.get("requirement_id")))
            if not isinstance(x.get("candidate_effect"), str) or len(x["candidate_effect"].strip()) < 25:
                fail(errors, "V2_VACUOUS_EFFECT:" + str(x.get("requirement_id")))

    # crosswalk rows
    import csv
    rows = list(csv.DictReader(crosswalk, delimiter="\t"))
    if len(rows) != 141:
        fail(errors, "CROSSWALK_TOTAL_NOT_141")
    v2rows = [r for r in rows if r.get("kind") == "addendum_requirement"]
    if len(v2rows) != 4 or tuple(r.get("id") for r in v2rows) != V2_IDS:
        fail(errors, "V2_CROSSWALK_ROWS")
    for r in v2rows:
        if not r.get("candidate_fate") or len(r["candidate_fate"].strip()) < 25:
            fail(errors, "V2_CROSSWALK_VACUOUS:" + str(r.get("id")))

    # D1: active specialist state must be received/adjudicated; historical plan is allowed only under historical_plan_only.
    sd = decision.get("specialist_dependency") or {}
    if sd.get("status") != "BOTH_RETURNS_RECEIVED_AND_ADJUDICATED":
        fail(errors, "D1_SPECIALIST_DEPENDENCY_NOT_RECEIVED")
    if decision.get("specialist_consumption", {}).get("status") != "BOTH_RETURNS_RECEIVED_AND_ADJUDICATED":
        fail(errors, "D1_SPECIALIST_CONSUMPTION_NOT_RECEIVED")
    if decision.get("final_selection_frozen") is not True:
        fail(errors, "D1_FINAL_NOT_FROZEN")
    if "PENDING_TWO_FROZEN_SPECIALIST_RETURNS" in json.dumps(sd.get("status", "")):
        fail(errors, "D1_STALE_PENDING")

    # D2: selected/conditional/held coherence.
    sel = decision.get("selected_design") or {}
    expect = {
        "prepared_session_first": True,
        "durable_index_status": "HELD_NOT_SELECTED",
        "fresh_session_scan_removed": False,
        "second_i02_removed_unconditionally": False,
        "jsonl_removed_unconditionally": False,
        "q2_must_originate_from_source_stream": True,
    }
    for k, v in expect.items():
        if sel.get(k) != v:
            fail(errors, "D2_SELECTED_DESIGN:" + k)
    if not str(sel.get("construction_one_journal_one_certificate", "")).startswith("CONDITIONAL"):
        fail(errors, "D2_ONECERT_NOT_CONDITIONAL")
    if "REQUIRED" not in str(sel.get("second_certificate_fallback", "")):
        fail(errors, "D2_FALLBACK_MISSING")
    pa = decision.get("physical_architecture") or {}
    if "Prepared-session-first" not in str(pa.get("name", "")):
        fail(errors, "D2_PHYSICAL_NAME")
    if "Single-certification canonical C11 estate + immutable derived access index" in str(pa.get("name", "")):
        fail(errors, "D2_STALE_SC_ESTATE")
    layers = {x.get("id"): x for x in pa.get("layers", []) if isinstance(x, dict)}
    if "SELECTED" not in str(layers.get("L3_PREPARED_S", {}).get("status", "")):
        fail(errors, "D2_PREPARED_LAYER")
    if "HELD" not in str(layers.get("L7_DURABLE_INDEX", {}).get("status", "")):
        fail(errors, "D2_INDEX_LAYER")
    if "CONDITIONAL" not in str(layers.get("L5_CONSTRUCTION_CONDITIONAL", {}).get("status", "")):
        fail(errors, "D2_CONSTRUCTION_LAYER")
    seq = decision.get("implementation_sequence") or []
    if not seq or any("status" not in s for s in seq):
        fail(errors, "D2_SEQUENCE_STATUS")
    for s in seq:
        st = str(s.get("status", ""))
        act = str(s.get("action", ""))
        if "durable index" in act.lower() and not ("HELD" in st or "CONDITIONAL" in st):
            fail(errors, "D2_UNCONDITIONAL_INDEX_STEP")
        if ("one i02" in act.lower() or "one-certificate" in act.lower()) and "CONDITIONAL" not in st:
            fail(errors, "D2_UNCONDITIONAL_ONECERT_STEP")
    effects = decision.get("per_requirement_candidate_effect") or []
    emap = {x.get("requirement_id"): x.get("candidate_effect", "") for x in effects if isinstance(x, dict)}
    if tuple(emap) != BASE_IDS or len(emap) != 16:
        fail(errors, "D2_BASE_EFFECT_IDS")
    for k, v in emap.items():
        if len(v.strip()) < 25:
            fail(errors, "D2_VACUOUS_EFFECT:" + k)
        for bad in FORBIDDEN_EFFECTS:
            if bad.lower() in v.lower():
                fail(errors, "D2_STALE_EFFECT:" + k)
    ids = decision.get("identity_dispositions") or []
    if len(ids) != 118:
        fail(errors, "IDENTITY_COUNT_NOT_118")

    result = {
        "status": "PASS_V2_SUPPLEMENTARY_STRUCTURAL_20_REQUIREMENTS_118_IDENTITIES" if not errors else "REFUSE_V2_SUPPLEMENTARY",
        "errors": sorted(set(errors)),
        "base_requirements": 16,
        "v2_requirements": 4,
        "total_requirements": 20,
        "identity_dispositions": len(ids),
        "accepted_guard": accepted,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
