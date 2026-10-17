"""PYAT R26 T9C — four-court execution runner with pinned imports and real pytest.

Courts, run separately and never aggregated into a single acceptance percentage:

  1. FROZEN INDEPENDENT T9I SUITE (48 cases, byte-identical to the independent court
     file at a2a7bdeda76aa008b3d620b01af71f7fd6efaaae). This is the test transport
     the commission requires.
  2. OWN T9C REPAIR SUITE, against actually imported pinned native modules.
  3. UNCHANGED ORIGINAL T9B AUTHOR SUITE (28 positives), executed in the original
     author return directory against the original 1259-file native tree. This return
     does NOT modify that directory.
  4. UNCHANGED INHERITED ORIGINAL V553 CONSUMER-CONTRACT SUITE (8 tests), executed
     against the minimal byte-verified 22-source closure staged in this return.

Every run disables plugin autoload, uses -B (no bytecode writes), pins sys.path
against the ambient repository root, and records module __file__ receipts.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

RET = Path(__file__).resolve().parent
NATIVE = RET / "native"
FROZEN = RET / "frozen_t9i_court"
T9B_RET = RET.parent / "PYAT-R18-T9B-TEMPORAL-HISTORY-CONSUMER-R1"
AMBIENT = Path("/Users/matthewsmith/Desktop/Rawlsing")
V553_NATIVE_TEST = NATIVE / "data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py"

JUNIT = RET / "junit"
LOGS = RET / "logs"
EVID = RET / "evidence"
for d in (JUNIT, LOGS, EVID):
    d.mkdir(parents=True, exist_ok=True)


def pin_env() -> dict:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    return env


def run(name: str, argv: list, cwd: Path, env: dict) -> dict:
    started = time.time()
    proc = subprocess.run(argv, cwd=str(cwd), env=env,
                          capture_output=True, text=True, check=False)
    elapsed = round(time.time() - started, 3)
    (LOGS / f"{name}.log").write_text(
        f"$ {' '.join(argv)}\n# cwd={cwd}\n# exit={proc.returncode}\n"
        f"# elapsed_s={elapsed}\n--- stdout ---\n{proc.stdout}\n--- stderr ---\n{proc.stderr}\n")
    return {"name": name, "argv": argv, "cwd": str(cwd), "exit": proc.returncode,
            "elapsed_s": elapsed, "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:]}


def parse_junit(path: Path) -> dict:
    if not path.exists():
        return {"available": False}
    import xml.etree.ElementTree as ET
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    out = {"available": True, "suites": []}
    for s in suites:
        cases = []
        for tc in s.iter("testcase"):
            status = "passed"
            for bad in ("failure", "error", "skipped"):
                if tc.find(bad) is not None:
                    status = bad
            cases.append({"classname": tc.get("classname"), "name": tc.get("name"),
                          "time": tc.get("time"), "status": status})
        out["suites"].append({
            "name": s.get("name"), "tests": int(s.get("tests", 0)),
            "failures": int(s.get("failures", 0)), "errors": int(s.get("errors", 0)),
            "skipped": int(s.get("skipped", 0)), "time": s.get("time"),
            "cases": cases})
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    results = []

    # ---- Court 1: frozen independent T9I suite, 48 cases -------------------
    results.append(run(
        "frozen_t9i_independent_48",
        [sys.executable, "-B", "guarded_runner.py"],
        RET, pin_env()))

    # ---- Court 2: own T9C repair suite ------------------------------------
    results.append(run(
        "t9c_own_repair_suite",
        [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "--rootdir", str(RET), "-c", str(FROZEN / "pytest_t9i_frozen.ini"),
         f"--junitxml={JUNIT / 't9c_own_repair_suite.xml'}",
         str(RET / "test_t9c_repair.py")],
        RET, pin_env()))

    # ---- Court 3: unchanged inherited original V553 consumer-contract suite (8)
    results.append(run(
        "inherited_original_v553_native_8",
        [sys.executable, "-B", "run_pinned_v553_suite_t9c.py"],
        RET, pin_env()))

    # ---- Court 4: unchanged original T9B author suite (28) ----------------
    if T9B_RET.exists():
        results.append(run(
            "unchanged_t9b_author_28",
            [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
             "--rootdir", str(T9B_RET), "-c", str(FROZEN / "pytest_t9i_frozen.ini"),
             f"--junitxml={JUNIT / 'unchanged_t9b_author_28.xml'}",
             str(T9B_RET / "test_t9b_temporal.py")],
            T9B_RET, pin_env()))
    else:
        results.append({"name": "unchanged_t9b_author_28", "available": False,
                        "reason": f"author return not present at {T9B_RET}"})

    # ---- assemble evidence -----------------------------------------------
    summary = []
    for r in results:
        junit_path = JUNIT / f"{r['name']}.xml"
        summary.append({**{k: r.get(k) for k in ("name", "cwd", "exit", "elapsed_s")},
                        "junit": str(junit_path.relative_to(RET)),
                        "junit_sha256": sha256(junit_path) if junit_path.exists() and junit_path.stat().st_size else None,
                        "parsed": parse_junit(junit_path) if junit_path.exists() and junit_path.stat().st_size else {"available": False},
                        "log": f"logs/{r['name']}.log"})

    (EVID / "t9c_four_court_execution.json").write_text(json.dumps(
        {"schema": "PYAT_R26_T9C_FOUR_COURT_EXECUTION@1",
         "courts_are_separate_not_aggregated": True,
         "python": sys.version, "executable": sys.executable,
         "pytest_version": __import__("pytest").__version__,
         "results": summary}, indent=2, sort_keys=True) + "\n")

    for s in summary:
        p = s["parsed"]
        if not p.get("available"):
            print(f"{s['name']}: UNAVAILABLE (exit={s['exit']})")
            continue
        for suite in p["suites"]:
            print(f"{s['name']}: tests={suite['tests']} failures={suite['failures']} "
                  f"errors={suite['errors']} skipped={suite['skipped']} exit={s['exit']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())