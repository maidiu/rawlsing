#!/usr/bin/env python3
"""ZAK-00 v2 MCR-C: source-frozen original-task and output identity conservation.
This is a pre-dispatch contract court; it does NOT certify descendants' work.
"""
import argparse
import csv
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FLIGHTS = Path(__file__).resolve().parent / "FLIGHT_LAUNCHES"
FROZEN_AUTHOR = "9d24323494cc852ada078010f09bfcf9ceb911d9"
R2_INHERITANCE = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N020_LONG_MEMORY/VMESTYE/ZAKONCHILOC/ZAK_INHERITED_OBLIGATIONS.tsv"
AR_SEED = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/PROJECT_INHERITANCE_R1/CAMPAIGNS/N020_LONG_MEMORY/VMESTYE/DATA/LEGACY_AR58_SEED.tsv"
FULL_FAMILY_FLIGHTS = {1: (58, "release_id", AR_SEED),
                       8: (182, "zak_evidence_key", R2_INHERITANCE),
                       10: (182, "zak_evidence_key", R2_INHERITANCE),
                       11: (182, "zak_evidence_key", R2_INHERITANCE)}
BAD = re.compile("[\\u00ad\\u200b\\u200c\\u200d\\u2060\\ufeff]")
FLIGHT_RE = re.compile(r"^\\d+\\. (WORKER_RETURNS/[^\\n]+)$", re.M)
TASK_RE = re.compile(r"^[1-4]\\. (.+)$", re.M)

def git(*args):
    p = subprocess.run(["git", "-C", str(ROOT), *args],
                       capture_output=True, text=True, check=False)
    if p.returncode:
        raise AssertionError("git " + " ".join(args) + ": " + p.stderr[:220])
    return p.stdout

def source_bytes(path, commit):
    return git("show", commit + ":" + path)

def load_contract(text):
    match = re.search(r"MCR_COMPLETION_CONTRACT_BEGIN\\n(.*?)\\nMCR_COMPLETION_CONTRACT_END", text, re.S)
    if not match:
        raise AssertionError("missing completion contract")
    contract = {"MCR_SCOPE": [], "MCR_OBLIGATION": [], "MCR_RECEIVING": []}
    for line in match.group(1).splitlines():
        k, sep, obj = line.partition(": ")
        if not sep or k not in contract:
            raise AssertionError("unknown MCR-C record " + k)
        contract[k].append(json.loads(obj, object_pairs_hook=_reject_duplicate_keys))
    if len(contract["MCR_SCOPE"]) != 1 or len(contract["MCR_RECEIVING"]) != 1:
        raise AssertionError("one scope and receiving required")
    return contract, match.group(1)

def _reject_duplicate_keys(pairs):
    d = {}
    for k, v in pairs:
        if k in d:
            raise AssertionError("duplicate JSON key " + k)
        d[k] = v
    return d

def flight_path(n):
    return FLIGHTS / ("ZAK_%02d_FULL_COPY_PASTE_MCR.md" % n)

def required_ids(n, contract=None):
    if contract is None:
        contract, _ = load_contract(flight_path(n).read_text(encoding="utf-8"))
    scope = contract["MCR_SCOPE"][0]
    s = scope["source"]
    if n in FULL_FAMILY_FLIGHTS:
        expected, col, source = FULL_FAMILY_FLIGHTS[n]
        assert scope["expected_count"] == expected and scope["identity_columns"] == [col]
        assert s["path"] == source, (n, s["path"], source)
        rows = list(csv.DictReader(source_bytes(s["path"], s["commit"]).splitlines(), delimiter="\\t"))
        ids = [json.dumps([row[col]], ensure_ascii=False, separators=(",", ":")) for row in rows]
    else:
        assert "identity_columns" not in scope
        ids = [item["id"] for item in contract["MCR_OBLIGATION"]]
        assert scope["expected_count"] == len(ids)
    assert len(set(ids)) == len(ids) == scope["expected_count"], (n, len(ids), scope["expected_count"])
    return ids

def validate_one(n, text=None):
    path = flight_path(n)
    current = text if text is not None else path.read_text(encoding="utf-8")
    old = source_bytes(path.relative_to(ROOT).as_posix(), FROZEN_AUTHOR)
    orig_tasks = TASK_RE.findall(old[old.index("REQUIRED POSITIVE/NEGATIVE/CONSUMER CHALLENGE"):
                                 old.index("DELIVERABLE FILES")])
    orig_outputs = FLIGHT_RE.findall(old[old.index("DELIVERABLE FILES"):old.index("ENGINEERING COURT")])
    orig_outputs = [p.replace("\\u00ad", "") for p in orig_outputs]
    assert len(orig_tasks) == 4 and 3 <= len(orig_outputs) <= 4
    contract, raw = load_contract(current)
    assert not BAD.search(current), "hidden Unicode"
    assert "315251451a6d112fb312a6e80b096d345c5de6" not in current, "D01 invalid commit"
    assert not re.search(r"(?<![0-9a-f])[0-9a-f]{30,39}(?![0-9a-f])", current, re.I), "truncated source hash"
    assert not re.search(r"(?<![A-Za-z0-9])[0-9a-f]{8}\\.\\.\\.", current, re.I), "abbreviated digest"
    assert len(contract["MCR_OBLIGATION"]) == 5 + len(orig_outputs), (n, "task or output omitted")
    records = {item["id"]: item for item in contract["MCR_OBLIGATION"]}
    assert len(records) == len(contract["MCR_OBLIGATION"]), "duplicate obligation"
    for j, task in enumerate(orig_tasks, 1):
        key = "ZAK%02d-TASK-%02d" % (n, j)
        assert records[key].get("baseline_requirement") == task, (key, "old task modified, omitted, or truncated")
        assert records[key]["positive"].startswith("PASS=")
        assert records[key]["negative"].startswith("RED=")
        assert records[key]["positive"] != records[key]["negative"]
        assert records[key]["failure"] == "INCOMPLETE"
        assert records[key]["source"].get("blob") and len(records[key]["source"]["blob"]) == 40
    hostile = records["ZAK%02d-HOSTILE" % n]
    assert hostile.get("baseline_requirement", "").startswith("NEW REVIEW NEGATIVE"), "hostile case absent"
    for j, opath in enumerate(orig_outputs, 1):
        key = "ZAK%02d-OUTPUT-%02d" % (n, j)
        rec = records[key]
        assert rec["baseline_output"] == opath and rec["output"] == opath, (key, "original deliverable omitted/renamed")
        assert rec["positive"].startswith("PASS=") and rec["negative"].startswith("RED=")
        assert rec["failure"] == "INCOMPLETE"
    ids = required_ids(n, contract)
    assert contract["MCR_RECEIVING"][0]["author_ceiling"] == "DELIVERED_PENDING_RECEIVING"
    assert contract["MCR_RECEIVING"][0]["on_any_failure"] == "INCOMPLETE"
    if n == 1:
        assert "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13" in current, "D03 AR0005 absent"
        assert "a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b" in current, "D03 AR0006 absent"
    if n in (2, 8):
        assert "V552J" in raw and "12" in raw and "F03" in raw, "D05-D07 J/F03 near positive omitted"
    if n == 2:
        assert "BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR" in raw, "D07 V552 scoring/coverage separation missing"
    if n == 8:
        assert "LMX-043" in raw and "LMQ-001" in raw and "LMQ-009" in raw, "D04 lifecycle and parity debts dropped"
    return {"flight": n, "tasks": 4, "hostile": 1, "outputs": len(orig_outputs),
            "obligations": len(records), "coverage_identity_count": len(ids), "status": "PASS_AUTHOR_CONTRACT_COMPLETENESS_NOT_EXECUTED_DESCENDANTS"}

def self_test():
    s = flight_path(11).read_text(encoding="utf-8")
    assert validate_one(11)["obligations"] == 8
    for mutant in [
        s.replace("ZAK11-TASK-01", "ZAK11-OMITTED-01", 1),
        s.replace("EPISTEMIC_GRADE_MATRIX.tsv", "EPIS\\u00adTEMIC_GRADE_MATRIX.tsv", 1),
        s.replace("ZAK11-OUTPUT-02", "ZAK11-TASK-01", 1),
    ]:
        try:
            validate_one(11, mutant)
        except (AssertionError, KeyError, ValueError):
            pass
        else:
            raise AssertionError("negative mutant passed")
    return "PASS 3/3 claim/filename/duplicate mutants rejected"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--flight", type=int, choices=range(1, 12))
    p.add_argument("--all", action="store_true")
    p.add_argument("--enumerate-expected", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args()
    if args.self_test:
        print(self_test())
        return
    if args.enumerate_expected:
        assert args.flight
        print("\\n".join(required_ids(args.flight)))
        return
    reports = [validate_one(n) for n in (range(1, 12) if args.all else [args.flight])]
    print(json.dumps(reports, indent=2))

if __name__ == "__main__":
    main()
