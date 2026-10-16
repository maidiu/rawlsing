#!/usr/bin/env python3
"""OC7 independent court runner.

Runs each frozen suite unchanged against a given pinned module variant and
records real JUnit XML + stdout. Counts come from the JUnit XML, not from
pytest's exit code (pytest returns nonzero for genuine frozen-oracle REDs,
which must be preserved, not suppressed).

Usage: run_court.py <before|after> <evidence_subdir>
"""
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET

SRC = {
    "before": "/tmp/oc7-before/source",
    "after": "/tmp/oc7-after/source",
}
AUTH = os.environ["OC7_CONFTEST"]

SUITES = [
    ("inherited_131", [
        "test_custody_hostiles.py",
        "test_positive_lifecycle.py",
        "test_ocr1_independent_hostile.py",
        "test_oc2_regressions.py",
        "test_oc3_independent_hostile.py",
    ]),
    ("oc4_new_36", ["test_oc4_repair_controls.py"]),
    ("oc5_prior_23", ["test_oc5_prior_predictions.py"]),
    ("oc5e_native_159", ["test_oc5e_native_hostiles.py"]),
]

# Only executed for the AFTER variant: OC6's own new author controls.
SUITES_AFTER_ONLY = [("oc6_author_273", ["test_oc6_author_controls.py"])]


def run_suite(src, name, files, outdir):
    junit = os.path.join(outdir, f"{name}.xml")
    log = os.path.join(outdir, f"{name}.log")
    cmd = [sys.executable, "-m", "pytest", "-p", "no:cacheprovider",
           "--junitxml", junit, "-v", "--tb=short", "-rA", *files]
    proc = subprocess.run(cmd, cwd=src, capture_output=True, text=True)
    with open(log, "w") as fh:
        fh.write("$ " + " ".join(cmd) + "\n")
        fh.write(f"# cwd={src}\n")
        fh.write(f"# exit={proc.returncode}\n")
        fh.write(proc.stdout)
        fh.write("\n--- STDERR ---\n")
        fh.write(proc.stderr)
    tree = ET.parse(junit)
    root = tree.getroot()
    suites = root.findall("testsuite") or [root]
    total = failures = errors = skipped = 0
    cases = []
    for ts in suites:
        total += int(ts.get("tests", 0))
        failures += int(ts.get("failures", 0))
        errors += int(ts.get("errors", 0))
        skipped += int(ts.get("skipped", 0))
        for tc in ts.findall("testcase"):
            bad = tc.find("failure") is not None or tc.find("error") is not None
            cases.append({
                "id": f"{tc.get('classname')}::{tc.get('name')}",
                "verdict": "RED" if bad else ("SKIP" if tc.find("skipped") is not None else "PASS"),
            })
    return {
        "suite": name, "files": files, "exit": proc.returncode,
        "tests": total, "PASS": total - failures - errors - skipped,
        "RED": failures + errors, "SKIP": skipped,
        "junit": os.path.relpath(junit, outdir), "log": os.path.relpath(log, outdir),
        "cases": cases,
    }


def main():
    variant, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    src = SRC[variant]
    results = []
    suites = list(SUITES) + (SUITES_AFTER_ONLY if variant == "after" else [])
    for name, files in suites:
        r = run_suite(src, name, files, outdir)
        results.append(r)
        print(f"[{variant}] {name:20s} tests={r['tests']:4d} PASS={r['PASS']:4d} "
              f"RED={r['RED']:3d} SKIP={r['SKIP']:2d} exit={r['exit']}")
    tot = sum(r["tests"] for r in results)
    totp = sum(r["PASS"] for r in results)
    totr = sum(r["RED"] for r in results)
    tots = sum(r["SKIP"] for r in results)
    print(f"[{variant}] {'TOTAL':20s} tests={tot:4d} PASS={totp:4d} RED={totr:3d} SKIP={tots:2d}")
    with open(os.path.join(outdir, "court_summary.json"), "w") as fh:
        json.dump({"variant": variant, "src": src, "suites": results,
                   "total": {"tests": tot, "PASS": totp, "RED": totr, "SKIP": tots}},
                  fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
