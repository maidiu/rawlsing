"""Run the INHERITED F6C / F6M suites unmodified, cold, with real JUnit.

NO TEST IS EDITED, SKIPPED, PATCHED OR RELAXED. Test files are staged at their
exact pinned Git blobs and executed as-is.

One custody control is required and is recorded explicitly rather than hidden:
``preimport_pinned_producer()`` imports the repaired producer BEFORE pytest
runs collection. Reason, verified in this court: the F6 candidate packages are
namespace packages (``rawlsing_next`` has no ``__init__.py``), and their
portions are split across the test-run directory and the candidate directory.
pytest mutates ``sys.path`` during collection, after which the
``rawlsing_next`` namespace portion that holds the producer is no longer
reachable and collection dies with ModuleNotFoundError before a single test
runs. Pre-importing pins the correct pinned blob into ``sys.modules``. This is
a transport fix, identical in kind to the "preimports WP2's exact repaired
producer before loading unchanged original tests" control WP2I already
recorded. It grants no rights and relaxes no assertion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN = HERE.parent
W = "WORKER_RETURNS/PYAT-R32-WP2-NATIVE-WORLD-POSSIBILITY-R1"
F6M = RETURN / "02_TESTS" / W / "inherited" / "F6M"
OUT = RETURN / "03_EXECUTABLE_JUNIT_AND_TWO_COLD"

PINNED = {
    "candidate/rawlsing_next/pre553_heterogeneous_synthesis.py":
        "2df811d76db258d98d89ffb43c830cb221ff9a7d",
    "candidate/rawlsing_next/pre553_empirical_objects.py":
        "a61365b994e5c3c50de0f598fcf40e90abf757b6",
    "inherited/F6C/02_TESTS/f6c_worlds.py":
        "52c3dfe30dd807d79a67761a37c7d79214caacdd",
    "inherited/F6C/02_TESTS/run/rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py":
        "07f405033e4703b1a0ddc710cffd529383561d1f",
    "tests/test_consumer_repair.py":
        "f6110081834330ce0343021d2dbd3f078ef48840",
    "inherited/F6L/02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json":
        None,
}

PREIMPORT = """
import sys
sys.path[:0] = [
    r'{f6m}/candidate',
    r'{f6m}/candidate/rawlsing_next',
    r'{f6m}/inherited/F6C/02_TESTS',
]
import rawlsing_next.pre553_heterogeneous_synthesis as _m
import rawlsing_next.pre553_empirical_objects as _o
sys.stderr.write('PREIMPORT_OK %s %s\\n' % (_m.__file__, _o.__file__))
import pytest
raise SystemExit(pytest.main(sys.argv[1:]))
"""

SUITES = {
    "f6m_repair_20": {
        "cwd": F6M,
        "test": "tests/test_consumer_repair.py",
        "pythonpath": [F6M / "candidate", F6M / "candidate/rawlsing_next/tests",
                       F6M / "candidate/rawlsing_next", F6M / "inherited/F6C/02_TESTS"],
        "label": "inherited F6M decision/admission repair tests (20)",
    },
    "f6m_original35": {
        "cwd": F6M / "inherited/F6C/02_TESTS/run",
        "test": "rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py",
        "pythonpath": [F6M / "candidate", F6M / "candidate/rawlsing_next/tests",
                       F6M / "candidate/rawlsing_next", F6M / "inherited/F6C/02_TESTS"],
        "label": "inherited original F6 heterogeneous synthesis suite (24 cases + 11 subtests = 35 events)",
    },
}


def verify_blobs():
    bad = []
    for rel, expect in PINNED.items():
        p = F6M / rel
        b = p.read_bytes()
        got = hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()
        if expect and got != expect:
            bad.append((rel, got, expect))
    return bad


def junit_counts(xml):
    import xml.etree.ElementTree as ET
    root = ET.parse(xml).getroot()
    suites = [root] if root.tag == "testsuite" else list(root)
    tc = sum(int(s.get("tests", 0)) for s in suites)
    fa = sum(int(s.get("failures", 0)) for s in suites)
    er = sum(int(s.get("errors", 0)) for s in suites)
    sk = sum(int(s.get("skipped", 0)) for s in suites)
    return {"tests": tc, "failures": fa, "errors": er, "skipped": sk,
            "passed": tc - fa - er - sk}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    bad = verify_blobs()
    receipt = {
        "record": "PYAT-R35-F6C-INHERITED-SUITE-REPLAY@1",
        "test_rewrite": "NONE. Every suite runs at its exact pinned Git blob.",
        "pinned_blob_mismatches": bad,
        "custody_control": {
            "name": "preimport_pinned_producer",
            "why": ("rawlsing_next is a namespace package with no __init__.py; its "
                    "portions are split between the test-run directory and the "
                    "candidate directory. pytest mutates sys.path during collection, "
                    "after which the producer's namespace portion is unreachable and "
                    "collection aborts with ModuleNotFoundError before any test runs."),
            "what_it_does": ("imports the pinned repaired producer from its candidate "
                             "directory before pytest collection begins"),
            "what_it_does_not_do": ("does not modify, skip, patch or relax any test, "
                                    "assertion or fixture; grants no right"),
        },
        "suites": {},
    }
    for name, s in SUITES.items():
        if a.only and a.only != name:
            continue
        xml = OUT / f"{name}.xml"
        env = dict(os.environ)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        env["PYTHONPATH"] = os.pathsep.join(str(p) for p in s["pythonpath"])
        cmd = [sys.executable, "-B", "-c", PREIMPORT.format(f6m=F6M),
               "-q", s["test"], "--import-mode=importlib", "-p", "no:cacheprovider",
               "--junitxml", str(xml)]
        proc = subprocess.run(cmd, cwd=str(s["cwd"]), env=env,
                              capture_output=True, text=True)
        counts = junit_counts(xml) if xml.exists() else None
        receipt["suites"][name] = {
            "label": s["label"],
            "argv_shape": ["python3", "-B", "<preimport driver>", "-q", s["test"],
                           "--import-mode=importlib", "-p", "no:cacheprovider",
                           "--junitxml", xml.name],
            "cwd": str(s["cwd"]),
            "pythonpath": [str(p) for p in s["pythonpath"]],
            "returncode": proc.returncode,
            "junit": counts,
            "junit_file": str(xml.relative_to(RETURN.parent.parent.parent)),
            "preimport_line": next((l for l in proc.stderr.splitlines()
                                    if l.startswith("PREIMPORT_OK")), None),
            "stdout_tail": proc.stdout.strip().splitlines()[-3:],
        }
        print(f"{name}: rc={proc.returncode} {counts}")
        for l in proc.stdout.strip().splitlines()[-3:]:
            print("   ", l)
    (OUT / "inherited_suite_replay_receipt.json").write_text(json.dumps(receipt, indent=2))
    print("wrote", OUT / "inherited_suite_replay_receipt.json")


if __name__ == "__main__":
    main()