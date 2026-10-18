"""GF1N Phase B independent suite runner.

Runs every frozen predecessor court against the exact GF1M follow-up candidate
seated at the original runtime consumer seat.  Raw JUnit and logs are retained;
counts are recomputed from the XML testcase elements, never copied from prose.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

R = Path(__file__).resolve().parents[1]
OUT = R / "03_REAL_FROZEN_JUNIT_AND_COLD"
OUT.mkdir(parents=True, exist_ok=True)
S = R / "stage"
E = S / "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1"
G = S / "WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1"
H = S / "WORKER_RETURNS/PYAT-R32-GF1H-PAIR-CONSUMER-INTEGRITY-REPAIR-R1"
J = S / "WORKER_RETURNS/PYAT-R32-GF1J-INDEPENDENT-GF1H-COURT-R1"
K = S / "WORKER_RETURNS/PYAT-R33-GF1K-CATEGORY-IDENTITY-REPAIR-R1"
F = S / "WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1"
I = S / "WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1"
V = S / "WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1"
REPRO = E / "court/repro"

ENV = dict(os.environ,
           PYTHONDONTWRITEBYTECODE="1",
           PYTEST_DISABLE_PLUGIN_AUTOLOAD="1",
           GF1G_COURT=str(E), GF1G_ORACLE=str(G / "01_FROZEN_ORACLE.json"),
           GF1J_GF1G_TEST=str(G / "phase_a/test_gf1g_precommitted.py"),
           GF1H_COURT=str(E), GF1H_GF1G=str(G),
           GF1K_COURT=str(E), GF1K_GF1G=str(G),
           GF1M_HISTORICAL_HELPER=str(V / "phase_a/test_gf1l_executable_v2.py"),
           GF1M_ORIGINAL_PHASE_A=str(R / "phase_b/test_independent_domains.py"))

SUITES = [
    ("frozen26_independent", R / "phase_b/test_independent_domains.py", REPRO, 26),
    ("author22_followup", R / "phase_b/test_nonfinite_refusal.py", REPRO, 22),
    ("original44", E / "court/repro/test_gf1_generic_pair.py", REPRO, 44),
    ("gf1g26_frozen", G / "phase_a/test_gf1g_precommitted.py", REPRO, 26),
    ("gf1h26_frozen", H / "test_gf1h_adversarial.py", REPRO, 26),
    ("gf1j3_native", J / "repro/test_gf1j_postfreeze_native_identity_hostiles.py", REPRO, 3),
    ("gf1l14_frozen", V / "phase_a/test_gf1l_executable_v2.py", REPRO, 14),
    ("gf1l10_supplemental", V / "postinspection/test_gf1l_typed_domain_conservation.py", REPRO, 10),
    ("gf1k12_author", K / "test_gf1k_native_identity.py", REPRO, 12),
    ("guard26_storage", V / "repair/test_storage_guard.py", REPRO, 26),
    ("historical_gf1f100", F / "tests/test_gf1f_independent_consumer.py", F, 100),
    ("historical_gf1i19", I / "court/test_gf1i_independent.py", I / "court", 19),
]


def counts(xml: Path) -> dict:
    root = ET.parse(xml).getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))
    out = {k: sum(int(s.attrib.get(k, 0)) for s in suites)
           for k in ("tests", "failures", "errors", "skipped")}
    failed = [c.attrib.get("name") for c in root.iter("testcase")
              if c.find("failure") is not None or c.find("error") is not None]
    out["failed_nodes"] = failed
    return out


def main() -> int:
    receipts = []
    for name, test, cwd, expected in SUITES:
        if not Path(test).is_file():
            receipts.append({"name": name, "status": "MISSING_TEST", "path": str(test)})
            continue
        xml = OUT / (name + ".xml")
        log = OUT / (name + ".log")
        args = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
                "--import-mode=importlib", str(test), "--junitxml=" + str(xml)]
        proc = subprocess.run(args, cwd=cwd, env=ENV, text=True, capture_output=True)
        log.write_text(proc.stdout + proc.stderr)
        got = counts(xml) if xml.is_file() else None
        receipts.append({"name": name, "command": args, "cwd": str(cwd),
                         "exit": proc.returncode, "expected_tests": expected,
                         "counts": got,
                         "test_count_matches": bool(got and got["tests"] == expected)})
        print(name, "exit", proc.returncode, got, flush=True)
    (R / "phase_b/SUITE_RECEIPTS.json").write_text(json.dumps(receipts, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
