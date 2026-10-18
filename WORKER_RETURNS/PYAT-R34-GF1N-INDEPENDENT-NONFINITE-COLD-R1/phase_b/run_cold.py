"""GF1N two-process cold bit-equivalence for the independent hostile cases."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

R = Path(__file__).resolve().parents[1]
S = R / "stage"
E = S / "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1"
G = S / "WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1"
WORKER = R / "phase_a/gf1n_cold_worker.py"
OUT = R / "03_REAL_FROZEN_JUNIT_AND_COLD"
CASES = ["native_positive", "finite_heterogeneous_condition", "finite_heterogeneous_target",
         "nonfinite_plus_infinity_condition", "nonfinite_minus_infinity_target",
         "nonfinite_nan_condition", "signed_zero_target", "collision_int_string_condition",
         "support_exceeds_risk", "typed_missing_target", "observed_zero"]
NONFINITE = {"nonfinite_plus_infinity_condition", "nonfinite_minus_infinity_target",
             "nonfinite_nan_condition"}


def run(case: str, seed: str) -> dict:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONHASHSEED=seed,
               GF1G_COURT=str(E), GF1G_ORACLE=str(G / "01_FROZEN_ORACLE.json"),
               GF1G_CONTRACT=str(G / "phase_a/test_gf1g_precommitted.py"))
    proc = subprocess.run([sys.executable, "-B", str(WORKER), case],
                          cwd=E / "court/repro", env=env, text=True, capture_output=True)
    line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    if not line:
        raise RuntimeError("cold worker produced no JSON: exit=" + str(proc.returncode)
                           + " stderr=" + proc.stderr[-2000:])
    payload = json.loads(line)
    payload.pop("pid", None)
    payload.pop("python", None)
    return {"exit": proc.returncode, "payload": payload,
            "stderr": proc.stderr[-1000:]}


def main() -> int:
    receipts = []
    failures = []
    for case in CASES:
        a = run(case, "0")
        b = run(case, "1")
        same = a["payload"] == b["payload"]
        outcome = a["payload"].get("outcome", "")
        ok = (a["exit"] == 0 and b["exit"] == 0 and same
              and not outcome.startswith("UNTYPED")
              and a["payload"].get("strict_ok") is not False)
        if case in NONFINITE:
            ok = ok and outcome in ("CONSUMER_REFUSED", "CONSTRUCTION_REFUSED", "HOLD")
        if case == "native_positive":
            ok = ok and outcome == "ACCEPTED" and a["payload"].get("contract_ok") is True
        if not ok:
            failures.append(case)
        receipts.append({"case": case, "outcome": outcome, "same_payload": same,
                         "first_exit": a["exit"], "second_exit": b["exit"],
                         "strict_ok": a["payload"].get("strict_ok"),
                         "contract_ok": a["payload"].get("contract_ok"),
                         "deterministic": a["payload"].get("deterministic"),
                         "payload_sha256": __import__("hashlib").sha256(
                             json.dumps(a["payload"], sort_keys=True).encode()).hexdigest(),
                         "ok": ok})
        print(case, outcome, "same", same, "ok", ok, flush=True)
    summary = {"schema": "PYAT_R34_GF1N_COLD_BIT_EQUIVALENCE@1",
               "cases": receipts, "failures": failures,
               "all_ok": not failures,
               "note": "two fresh OS processes with PYTHONHASHSEED 0 and 1; pid/python removed before comparison"}
    (OUT / "cold_hostile_bit_equivalence.json").write_text(json.dumps(summary, indent=2) + "\n")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
