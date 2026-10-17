"""F6J — physically execute every court with pinned imports and real pytest.

Courts, kept separate and never aggregated into one acceptance percentage:
  1. F6J independent frozen-world court (12 worlds, exact rational, pre-registered)
  2. F6J falsifier / admission / consumer attacks
  3. INHERITED original S03FO suite (24 tests)
  4. F6C AUTHOR court (57 tests) - reproduced, not accepted as science
  5. F6J new adversarial consumer tests

Every run pins sys.path to THIS return's byte-verified staged native, disables
plugin autoload, uses -B, and records module __file__ receipts.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
STAGE = RET / "01_STAGED_NATIVE"
TESTS = RET / "04_TESTS"
JUNIT = RET / "05_JUNIT"
LOGS = RET / "06_LOGS"
EVID = RET / "07_EVIDENCE"
for d in (JUNIT, LOGS, EVID):
    d.mkdir(parents=True, exist_ok=True)


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def env():
    e = dict(os.environ)
    e["PYTHONDONTWRITEBYTECODE"] = "1"
    e["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    # Pin the staged byte-verified native onto PYTHONPATH so the transported
    # candidate suites resolve rawlsing_next against THIS return's copy.
    e["PYTHONPATH"] = str(STAGE) + os.pathsep + e.get("PYTHONPATH", "")
    return e


def run(name, argv, cwd=None):
    t0 = time.time()
    p = subprocess.run(argv, cwd=str(cwd or RET), env=env(),
                       capture_output=True, text=True, check=False)
    el = round(time.time() - t0, 3)
    (LOGS / f"{name}.log").write_text(
        f"$ {' '.join(map(str, argv))}\n# cwd={cwd or RET}\n# exit={p.returncode}\n"
        f"# elapsed_s={el}\n--- stdout ---\n{p.stdout}\n--- stderr ---\n{p.stderr}\n")
    return {"name": name, "argv": [str(a) for a in argv], "exit": p.returncode,
            "elapsed_s": el, "stdout_tail": p.stdout[-3000:],
            "stderr_tail": p.stderr[-3000:]}


def parse(path):
    p = Path(path)
    if not p.exists() or not p.stat().st_size:
        return {"available": False}
    import xml.etree.ElementTree as ET
    root = ET.parse(p).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    out = {"available": True, "suites": []}
    for s in suites:
        cases = []
        for tc in s.iter("testcase"):
            st = "passed"
            for bad in ("failure", "error", "skipped"):
                if tc.find(bad) is not None:
                    st = bad
            cases.append({"classname": tc.get("classname"), "name": tc.get("name"),
                          "status": st})
        out["suites"].append({"name": s.get("name"), "tests": int(s.get("tests", 0)),
                              "failures": int(s.get("failures", 0)),
                              "errors": int(s.get("errors", 0)),
                              "skipped": int(s.get("skipped", 0)), "cases": cases})
    return out


def main():
    results = []
    base = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
            "-p", "no:randomly", "--rootdir", str(RET)]
    pin = f"--import-mode=importlib"

    results.append(run("f6j_independent_frozen_courts",
                       [sys.executable, "-B", "03_SCRIPTS/execute_native_vs_frozen.py"]))
    results.append(run("f6j_falsifier_attacks",
                       [sys.executable, "-B", "03_SCRIPTS/falsifier_attacks.py"]))
    results.append(run("f6j_admission_consumer_attacks",
                       [sys.executable, "-B", "03_SCRIPTS/admission_and_consumer_attacks.py"]))

    # inherited original S03FO suite (24 tests) against the staged byte-verified native
    results.append(run("inherited_s03fo_suite_24",
                       base + [pin, f"--junitxml={JUNIT/'inherited_s03fo_suite_24.xml'}",
                               str(TESTS / "run/rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py")]))

    # F6C author court (57) reproduced against the staged native.
    # The author suite contains a custody PATH-SUFFIX control that asserts the
    # producer module is loaded from the candidate's own 05_NATIVE_STAGE/ path.
    # Against this return's byte-identical staging that one control must fail; it
    # is a custody-location control, NOT a candidate defect. Both counts are
    # recorded.
    results.append(run("f6c_author_court_57",
                       base + [pin, f"--junitxml={JUNIT/'f6c_author_court_57.xml'}",
                               str(TESTS / "candidate_transport/test_f6c_frozen_court.py")]))

    # F6J new adversarial consumer tests
    results.append(run("f6j_new_adversarial_tests",
                       base + [pin, f"--junitxml={JUNIT/'f6j_new_adversarial_tests.xml'}",
                               str(TESTS / "test_f6j_adversarial.py")]))

    summary = []
    for r in results:
        jp = JUNIT / f"{r['name']}.xml"
        summary.append({**{k: r.get(k) for k in ("name", "exit", "elapsed_s")},
                        "junit": str(jp.relative_to(RET)) if jp.exists() else None,
                        "junit_sha256": sha256(jp) if jp.exists() else None,
                        "parsed": parse(jp),
                        "log": f"06_LOGS/{r['name']}.log"})

    receipts = {}
    for n in sorted(sys.modules):
        f = getattr(sys.modules[n], "__file__", None)
        if f and str(Path(f).resolve()).startswith(str(RET)):
            receipts[n] = str(Path(f).resolve().relative_to(RET))

    payload = {
        "schema": "PYAT_R27_F6J_ALL_COURTS_EXECUTION@1",
        "courts_are_separate_not_aggregated": True,
        "python": sys.version, "executable": sys.executable,
        "native_git_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
        "staged_native_sha256": sha256(STAGE / "rawlsing_next/pre553_heterogeneous_synthesis.py"),
        "staged_semantic_hash_sha256": sha256(STAGE / "rawlsing_next/pre553_empirical_objects.py"),
        "results": summary,
    }
    (EVID / "all_courts_execution.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n")

    for s in summary:
        p = s["parsed"]
        if not p.get("available"):
            print(f"{s['name']}: script only (exit={s['exit']})")
            continue
        for su in p["suites"]:
            print(f"{s['name']}: tests={su['tests']} failures={su['failures']} "
                  f"errors={su['errors']} skipped={su['skipped']} exit={s['exit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
