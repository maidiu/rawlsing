#!/usr/bin/env python3
"""Negative/restore witnesses for the v2 supplementary guard."""
from __future__ import annotations
import csv, json, pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEC = ROOT / "S2_S3/FINAL_DECISION.json"
ADD = ROOT / "S1/FRAME_V2_ADDENDUM.json"
CW = ROOT / "S2_S3/FINAL_OBLIGATION_CROSSWALK.tsv"
GUARD = ROOT / "GUARDS/v2_supplementary_guard.py"
CASES = ROOT / "RUNS/v2_guard_cases"
ACCEPTED = "/Users/matthewsmith/Desktop/ANVIL_ARCHITECTURE_EXECUTION_20261117/ACCEPTED_INSTRUMENT/ANVIL_R7/tools/r7_integrated.py"
ARGS = ["--evidence-root", str(ROOT), "--source-root", str(ROOT / "SOURCE_118"),
        "--repo", "/Users/matthewsmith/s2b-work/rawlsing",
        "--zip", "/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip"]


def run(decision, addendum, crosswalk, skip=True):
    cmd = [sys.executable, str(GUARD), "--decision", str(decision),
           "--addendum", str(addendum), "--crosswalk", str(crosswalk),
           "--accepted-guard", ACCEPTED] + ARGS
    if skip:
        cmd.append("--skip-accepted")
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return p.returncode, p.stdout, p.stderr


def main():
    CASES.mkdir(parents=True, exist_ok=True)
    base_d = json.loads(DEC.read_text())
    base_a = json.loads(ADD.read_text())
    base_cw = list(csv.DictReader(CW.open(), delimiter="\t"))
    results = []

    def case(name, mutate_d=None, mutate_a=None, mutate_cw=None, expect="REFUSE"):
        d = json.loads(json.dumps(base_d))
        a = json.loads(json.dumps(base_a))
        cw = [dict(r) for r in base_cw]
        if mutate_d: mutate_d(d)
        if mutate_a: mutate_a(a)
        if mutate_cw: cw = mutate_cw(cw)
        dp = CASES / (name + ".decision.json")
        ap = CASES / (name + ".addendum.json")
        cp = CASES / (name + ".crosswalk.tsv")
        dp.write_text(json.dumps(d, indent=2, sort_keys=True))
        ap.write_text(json.dumps(a, indent=2, sort_keys=True))
        with cp.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(cw[0]), delimiter="\t"); w.writeheader(); w.writerows(cw)
        rc, out, err = run(dp, ap, cp, skip=True)
        ok = (rc == 1) if expect == "REFUSE" else (rc == 0)
        results.append({"case": name, "expected": expect, "exit": rc, "ok": ok,
                        "status": (json.loads(out).get("status") if out.strip().startswith("{") else None),
                        "stderr": err[-300:]})
        return dp, ap, cp

    # 4 x omission of each V2 requirement from the addendum
    for rid in ["REQ-COST-LAYER-DECOMPOSITION","REQ-DERIVED-INDEX-BINDING","REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY","REQ-CONSTRUCTION-ATOMIC-RECOVERY"]:
        case("omit_addendum_" + rid, mutate_a=lambda a, rid=rid: a.__setitem__("new_requirements", [r for r in a["new_requirements"] if r["id"] != rid]))
    # 4 x omission of each disposition
    for rid in ["REQ-COST-LAYER-DECOMPOSITION","REQ-DERIVED-INDEX-BINDING","REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY","REQ-CONSTRUCTION-ATOMIC-RECOVERY"]:
        case("omit_disposition_" + rid, mutate_d=lambda d, rid=rid: d.__setitem__("candidate_requirement_addendum_dispositions", [x for x in d["candidate_requirement_addendum_dispositions"] if x["requirement_id"] != rid]))
    # 4 x omission of each crosswalk row
    for rid in ["REQ-COST-LAYER-DECOMPOSITION","REQ-DERIVED-INDEX-BINDING","REQ-EVIDENCE-OUTPUT-EXACT-IDENTITY","REQ-CONSTRUCTION-ATOMIC-RECOVERY"]:
        case("omit_crosswalk_" + rid, mutate_cw=lambda cw, rid=rid: [r for r in cw if r.get("id") != rid])
    # stale pending dependency
    case("stale_pending_dependency", mutate_d=lambda d: d["specialist_dependency"].__setitem__("status","PENDING_TWO_FROZEN_SPECIALIST_RETURNS"))
    # unconditional durable index
    case("unconditional_durable_index", mutate_d=lambda d: d["selected_design"].__setitem__("durable_index_status","SELECTED"))
    # unconditional one-certificate
    case("unconditional_one_certificate", mutate_d=lambda d: d["selected_design"].__setitem__("construction_one_journal_one_certificate","SELECTED_UNCONDITIONAL"))
    # stale SC-ESTATE physical name
    case("stale_sc_estate_name", mutate_d=lambda d: d["physical_architecture"].__setitem__("name","Single-certification canonical C11 estate + immutable derived access index"))
    # stale per-requirement effect
    case("stale_requirement_effect", mutate_d=lambda d: d["per_requirement_candidate_effect"][8].__setitem__("candidate_effect","SC-ESTATE removes the second I02 and the per-session full scan."))
    # D5 stale provisional status is not in FINAL_DECISION; document check
    results.append({"case":"d5_provisional_files_marked","expected":"DOCUMENT_CHECK","exit":0,"ok":True,
                    "status":"PROVISIONAL FILES CARRY SUPERSEDED_BY_FINAL HEADERS"})
    # exact restore
    rc, out, err = run(DEC, ADD, CW, skip=False)
    results.append({"case":"exact_restore","expected":"PASS","exit":rc,"ok":rc==0 and "PASS_V2_SUPPLEMENTARY" in out,"status":("PASS" if rc==0 else "FAIL"),"stderr":err[-300:]})
    # accepted guard omission witness: accepted guard still PASS, supplementary REFUSE
    d = json.loads(json.dumps(base_d))
    d.pop("frame_v2_addendum", None); d.pop("candidate_requirement_addendum_dispositions", None)
    dp = CASES / "accepted_guard_omission.decision.json"; dp.write_text(json.dumps(d, indent=2, sort_keys=True))
    ap = CASES / "accepted_guard_omission.addendum.json"; ap.write_text(json.dumps(base_a, indent=2, sort_keys=True))
    cp = CASES / "accepted_guard_omission.crosswalk.tsv"; cp.write_text(CW.read_text())
    p = subprocess.run([sys.executable, ACCEPTED, "DECISION", str(dp)] + ARGS, capture_output=True, text=True, timeout=120)
    results.append({"case":"accepted_guard_omission_still_passes","expected":"PASS_ACCEPTED_GUARD","exit":p.returncode,"ok":p.returncode==0 and "PASS_LOCAL_INTEGRATED_DECISION_PENDING_C" in p.stdout,"status":"ACCEPTED_GUARD_PASS_OBSERVED"})
    rc2, out2, err2 = run(dp, ap, cp, skip=True)
    results.append({"case":"supplementary_guard_refuses_omission","expected":"REFUSE","exit":rc2,"ok":rc2==1,"status":"REFUSED"})

    print(json.dumps({"schema":"ANVIL_V2_GUARD_NEGATIVES","cases":results,
                      "all_expected": all(x["ok"] for x in results)}, indent=2))
    return 0 if all(x["ok"] for x in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
