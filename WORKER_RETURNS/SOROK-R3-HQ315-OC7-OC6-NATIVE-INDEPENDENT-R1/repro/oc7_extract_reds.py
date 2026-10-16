#!/usr/bin/env python3
"""OC7 RED adjudication: extract the literal assertion each of the 21 AFTER REDs
makes, its before/after verdicts, and its actual failure text. Reviewer then
adjudicates each on that evidence. No test is edited, xfailed or suppressed."""
import json
import os
import xml.etree.ElementTree as ET

EV = "/tmp/oc7-evidence"


def load(variant):
    d = {}
    for fn in sorted(os.listdir(f"{EV}/{variant}")):
        if not fn.endswith(".xml"):
            continue
        root = ET.parse(f"{EV}/{variant}/{fn}").getroot()
        suites = root.findall("testsuite") or [root]
        for ts in suites:
            for tc in ts.findall("testcase"):
                key = f"{tc.get('classname')}::{tc.get('name')}"
                bad = tc.find("failure")
                if bad is not None:
                    d[key] = {
                        "verdict": "RED",
                        "file": fn,
                        "failure_text": (bad.text or "").strip(),
                        "failure_message": (bad.get("message") or "").strip(),
                    }
                elif tc.find("skipped") is not None:
                    d[key] = {"verdict": "SKIP", "file": fn}
                else:
                    d[key] = {"verdict": "PASS", "file": fn}
    return d


before = load("before")
after = load("after")
reds = sorted(k for k, v in after.items() if v["verdict"] == "RED")
rows = []
for k in reds:
    rows.append({
        "case": k,
        "before": before.get(k, {}).get("verdict", "ABSENT_BEFORE"),
        "after": "RED",
        "transition": ("UNCHANGED_HISTORICAL_RED" if before.get(k, {}).get("verdict") == "RED"
                       else "SUPERSEDED_HOLESAY_PASS_TO_RED"),
        "junit_file": after[k]["file"],
        "failure_message": after[k]["failure_message"],
        "failure_tail": "\n".join(after[k]["failure_text"].splitlines()[-14:]),
    })
out = {
    "after_red_total": len(reds),
    "unchanged_historical_red": sum(1 for r in rows if r["transition"] == "UNCHANGED_HISTORICAL_RED"),
    "superseded_passes_to_red": sum(1 for r in rows if r["transition"] == "SUPERSEDED_HOLESAY_PASS_TO_RED"),
    "rows": rows,
}
with open(f"{EV}/red_adjudication_raw.json", "w") as fh:
    json.dump(out, fh, indent=2)
for r in rows:
    print("=" * 100)
    print(f"{r['case']}\n  transition: {r['transition']}   ({r['junit_file']})")
    print("  message: " + r["failure_message"][:300])
