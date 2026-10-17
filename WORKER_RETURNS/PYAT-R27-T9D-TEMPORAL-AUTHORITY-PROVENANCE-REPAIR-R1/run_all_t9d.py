"""PYAT R27 T9D — real multi-court execution with pinned imports and real pytest.

Courts, run separately and never aggregated into a single acceptance percentage:

  1. FROZEN INDEPENDENT T9I SUITE (48)  — byte-identical T9I court, unchanged.
  2. T9C OWN REPAIR SUITE (52)          — byte-identical T9C suite + frozen T9C
                                          expected-output contract, unchanged.
  3. INHERITED ORIGINAL V553 NATIVE (8) — byte-identical consumer-contract suite.
  4. UNCHANGED ORIGINAL T9B AUTHOR (28) — byte-identical author suite + oracle +
                                          ledger + stored two-time artifact.
  5. T9R FROZEN DELTA (50)              — byte-identical T9R Phase A delta suite
                                          with T9D direct capability bindings.
  6. T9R POST-INSPECTION HOSTILES (7)   — byte-identical T9R falsifiers.
  7. T9D OWN AUTHORITY/PROVENANCE (22)  — productive-author repair checks.

Every court runs in a fresh process under `guarded_runner_t9d.py` with plugin
autoload disabled, bytecode writes disabled, explicit root/config, per-import
git blob SHA-1 (NUL preimage) checks, real JUnit and literal exits.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

RET = Path(__file__).resolve().parent
JUNIT = RET / "junit"
LOGS = RET / "logs"
EVID = RET / "evidence"
for d in (JUNIT, LOGS, EVID):
    d.mkdir(parents=True, exist_ok=True)

COURTS = [
    ("frozen_t9i_independent_48", "independent T9I frozen court (unchanged)"),
    ("t9c_own_repair_52", "T9C own repair suite (unchanged)"),
    ("inherited_original_v553_native_8", "original V553 consumer-contract suite (unchanged)"),
    ("unchanged_t9b_author_28", "original T9B author suite (unchanged)"),
    ("t9r_frozen_delta_50", "T9R frozen delta50 with T9D capability bindings"),
    ("t9r_postinspection_hostiles_7", "T9R post-inspection falsifiers (unchanged)"),
    ("t9d_own_authority_provenance", "T9D own authority/provenance repair checks"),
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_junit(path: Path) -> dict:
    if not path.exists() or not path.stat().st_size:
        return {"available": False}
    import xml.etree.ElementTree as ET
    root = ET.parse(path).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.iter("testsuite"))
    out = {"available": True, "suites": []}
    for s in suites:
        cases = []
        for tc in s.iter("testcase"):
            status = "passed"
            message = None
            for bad in ("failure", "error", "skipped"):
                node = tc.find(bad)
                if node is not None:
                    status = bad
                    message = (node.get("message") or "")[:500]
            cases.append({"classname": tc.get("classname"), "name": tc.get("name"),
                          "status": status, "message": message})
        out["suites"].append({
            "name": s.get("name"), "tests": int(s.get("tests", 0)),
            "failures": int(s.get("failures", 0)), "errors": int(s.get("errors", 0)),
            "skipped": int(s.get("skipped", 0)), "cases": cases})
    return out


def main() -> int:
    rows = []
    for suite, label in COURTS:
        cmd = [sys.executable, "-B", str(RET / "guarded_runner_t9d.py"), suite]
        started = time.time()
        proc = subprocess.run(cmd, cwd=str(RET), capture_output=True, text=True,
                              check=False,
                              env={**dict(__import__("os").environ),
                                   "PYTHONDONTWRITEBYTECODE": "1",
                                   "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"})
        elapsed = round(time.time() - started, 3)
        (LOGS / f"{suite}.log").write_text(
            f"$ {' '.join(cmd)}\n# cwd={RET}\n# exit={proc.returncode}\n"
            f"# elapsed_s={elapsed}\n--- stdout ---\n{proc.stdout}\n"
            f"--- stderr ---\n{proc.stderr}\n")
        junit_path = JUNIT / f"{suite}.xml"
        parsed = parse_junit(junit_path)
        rows.append({"name": suite, "label": label, "command": cmd,
                     "cwd": str(RET), "exit": proc.returncode, "elapsed_s": elapsed,
                     "log": f"logs/{suite}.log",
                     "junit": f"junit/{suite}.xml",
                     "junit_sha256": sha256(junit_path) if junit_path.exists() else None,
                     "parsed": parsed})
        if parsed.get("available"):
            for s in parsed["suites"]:
                print(f"{suite}: tests={s['tests']} failures={s['failures']} "
                      f"errors={s['errors']} skipped={s['skipped']} exit={proc.returncode}")
        else:
            print(f"{suite}: JUnit UNAVAILABLE exit={proc.returncode}")

    (EVID / "t9d_seven_court_execution.json").write_text(json.dumps(
        {"schema": "PYAT_R27_T9D_SEVEN_COURT_EXECUTION@1",
         "courts_are_separate_not_aggregated": True,
         "python": sys.version, "executable": sys.executable,
         "pytest_version": __import__("pytest").__version__,
         "results": rows}, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
