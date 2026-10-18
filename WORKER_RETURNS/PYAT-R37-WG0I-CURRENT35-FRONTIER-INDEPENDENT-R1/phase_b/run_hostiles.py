"""WG0I Phase B runner: real JUnit, two-process cold court, WG0R comparison record."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

R = Path(__file__).resolve().parents[1]
OUT = R / "02_REAL_HOSTILE_JUNIT_AND_LOGS"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(R / "phase_b"))
import wg0i_oracle as O  # noqa: E402


def counts(xml: Path) -> dict:
    root = ET.parse(xml).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    out = {k: sum(int(s.attrib.get(k, 0)) for s in suites)
           for k in ("tests", "failures", "errors", "skipped")}
    out["failed_nodes"] = [c.attrib.get("name") for c in root.iter("testcase")
                           if c.find("failure") is not None or c.find("error") is not None]
    return out


def cold(seed: str) -> dict:
    env = dict(os.environ, PYTHONHASHSEED=seed, PYTHONDONTWRITEBYTECODE="1")
    proc = subprocess.run([sys.executable, "-B", str(R / "phase_b/wg0i_oracle.py"), "cold"],
                          cwd=R, env=env, text=True, capture_output=True)
    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    if not line:
        raise RuntimeError("cold run failed: " + proc.stderr[-1500:])
    return {"exit": proc.returncode, "payload": json.loads(line)}


def main() -> int:
    frontier = O.probe_frontier()
    (R / "phase_b/probe_frontier.json").write_text(json.dumps(frontier, indent=2) + "\n")
    xml = OUT / "wg0i_hostiles.xml"
    args = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
            "--import-mode=importlib", str(R / "phase_b/test_wg0i_hostiles.py"),
            str(R / "phase_b/test_wg0r_comparison.py"),
            "--junitxml=" + str(xml)]
    proc = subprocess.run(args, cwd=R, text=True, capture_output=True)
    (OUT / "wg0i_hostiles.log").write_text(proc.stdout + proc.stderr)
    junit = counts(xml) if xml.is_file() else None

    a = cold("0")
    b = cold("1")
    same = a["payload"] == b["payload"]
    matrix = [O.run_matrix_mutation(n) for n in sorted(O.MATRIX_EXPECT)]
    probe = [O.run_probe_mutation(n) for n in sorted(O.PROBE_EXPECT)]
    baseline = O.baseline()
    wg0r = O.wg0r_status()
    receipts = {
        "schema": "PYAT_R37_WG0I_HOSTILE_RECEIPTS@1",
        "oracle_digest_sha256": O.ORACLE["oracle_digest_sha256"],
        "item_ledger_sha256": O.ORACLE["item_census"]["identity_ledger"]["sha256"],
        "probe_frontier_sha256": hashlib.sha256(
            (R / "phase_b/probe_frontier.json").read_bytes()).hexdigest(),
        "baseline": baseline,
        "pytest": {"command": args, "exit": proc.returncode, "counts": junit},
        "matrix_mutations": matrix,
        "probe_mutations": probe,
        "cold": {"first_exit": a["exit"], "second_exit": b["exit"],
                 "identical": same,
                 "payload_sha256": hashlib.sha256(
                     json.dumps(a["payload"], sort_keys=True).encode()).hexdigest()},
        "wg0r": wg0r,
        "verdict": "PASS_CONSERVATION_AT_FROZEN_GRAIN__WG0R_CURRENT_FRONTIER_"
                   + ("PRESENT" if wg0r["output_present"] else "ABSENT__HOLD_FOR_COMPARISON"),
    }
    (R / "phase_b/02_HOSTILE_RECEIPTS.json").write_text(json.dumps(receipts, indent=2) + "\n")

    comparison = None
    cp = R / "phase_b/WG0R_COMPARISON.json"
    if cp.is_file():
        comparison = json.loads(cp.read_text())
    receipts["wg0r_comparison"] = comparison
    (R / "phase_b/02_HOSTILE_RECEIPTS.json").write_text(json.dumps(receipts, indent=2) + "\n")
    print(json.dumps({"pytest": junit, "matrix_detected": sum(1 for x in matrix if x["detected"]),
                      "probe_detected": sum(1 for x in probe if x["detected"]),
                      "cold_identical": same, "wg0r_present": wg0r["output_present"]}, indent=2))
    return 0 if (junit and junit["failures"] == 0 and junit["errors"] == 0 and same
                 and all(x["detected"] for x in matrix + probe)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
