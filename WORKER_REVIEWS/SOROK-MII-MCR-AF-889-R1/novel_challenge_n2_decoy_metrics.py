#!/usr/bin/env python3
"""Reviewer-owned novel challenge N2 — decoy P6 call + unconnected invented metrics.

Existing author attacks cover (a) a fully counterfeit adapter with no real P6
call and (b) fully forged 63/63 or 53/54 receipt sets.  Neither covers the MIXED
laundering case this probe targets: a GENUINE observed `run_p6.experience`
return whose authentic digest is used to certify invented, unconnected metric
fields and an unrelated scenario claim.  A real call is necessary but never
sufficient; metrics must be traceable to observed producer output.

Run: python3 -B novel_challenge_n2_decoy_metrics.py
Requires MCR_QUALIFIED_RUNTIME_ROOT / MCR_QUALIFIED_RUNTIME_SHA like the
author consumer trace (separately authenticated protected checkout).
"""
import argparse
import hashlib
import importlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = Path(os.environ.get("MCR_QUALIFIED_RUNTIME_ROOT", "")).resolve()
APPROVED = os.environ.get("MCR_QUALIFIED_RUNTIME_SHA", "")
P6 = RUNTIME_ROOT / "WORKER_RETURNS/SOROK-P6-ONE-LIVING-HOUSE-R1"


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                      default=str, separators=(",", ":")).encode()).hexdigest()


def authenticate():
    assert P6.is_dir(), "runtime checkout missing"
    ref = subprocess.run(["git", "-C", str(RUNTIME_ROOT), "rev-parse", "HEAD"],
                         capture_output=True, text=True)
    assert ref.returncode == 0 and ref.stdout.strip() == APPROVED, "runtime SHA not authenticated"
    for rel in ("SOROK-P6-ONE-LIVING-HOUSE-R1", "SOROK-P5-CONTINUOUS-EXPERIENCE-R1",
                "SOROK-P4-FIRST-FULL-MPC-R1"):
        p = RUNTIME_ROOT / "WORKER_RETURNS" / rel
        if str(p) not in sys.path:
            sys.path.insert(0, str(p))


def observed_call(state, command, **kw):
    """Real call under the reviewer profiler; returns the public result and observed frames."""
    authenticate()
    run_p6 = importlib.import_module("run_p6")
    calls = []

    def hook(frame, event, arg):
        if event == "call" and frame.f_code.co_filename.startswith(str(P6)):
            calls.append({"file": Path(frame.f_code.co_filename).name,
                          "function": frame.f_code.co_name})

    args = argparse.Namespace(command=command, request_id=None, **kw)
    old = sys.getprofile()
    try:
        sys.setprofile(hook)
        result = run_p6.experience(state, args, provider_mode="INJECTED")
    finally:
        sys.setprofile(old)
    return result, calls


def main():
    receipt = {"probe": "N2-DECOY-P6-CALL-UNCONNECTED-METRICS", "checks": []}

    def check(name, ok, detail=""):
        receipt["checks"].append({"name": name, "result": "PASS" if ok else "RED",
                                  "detail": detail})
        if not ok:
            receipt.setdefault("fired", []).append(name)

    with tempfile.TemporaryDirectory(prefix="mcr-n2-") as td:
        state = Path(td) / "world"

        # --- A: genuine observed P6 call (the decoy carrier) ---
        result, calls = observed_call(state, "new", situated_house=True)
        real_digest = digest(result)
        check("genuine_p6_return_observed",
              any(c["function"] == "experience" and c["file"] == "run_p6.py" for c in calls),
              f"{len(calls)} profiler frames")

        # --- B: invented metrics riding on the genuine digest ---
        laundered = {
            "p6_observed_return_sha256": real_digest,
            "e9_latency_p95_ms": 3, "e9_cold_start_ms": 41,
            "e3_exposure_ledger_writes": 2, "e8_replay_failures": 0,
            "proves": "MII-P03 unusual out-of-profile target recognition",
        }
        metric_evidence = [c for c in calls
                           if any(k in c["function"].lower() for k in ("latency", "perf", "exposure", "replay"))]
        check("invented_metrics_have_no_observed_producer", not metric_evidence,
              "no profiled frame produces latency/exposure/replay data")
        narration_text = json.dumps(result.get("narration", []), default=str)
        unrelated_proven = "P03" in narration_text or result.get("recognized_identity") not in (None, "")
        check("unrelated_scenario_claim_not_in_real_return", not unrelated_proven,
              f"recognized_identity={result.get('recognized_identity')!r}")
        check("laundered_receipt_must_be_rejected",
              not metric_evidence and not unrelated_proven)

        # --- C: decoy direction — real call on a DIFFERENT scenario ---
        look, look_calls = observed_call(state, "look", target="bench")
        check("decoy_real_call_on_bench_yields_no_sandal_recognition",
              "sandals" not in (look.get("recognition") or {}),
              json.dumps(look.get("recognition"), default=str))
        check("decoy_call_cannot_certify_sandal_identity",
              look.get("recognized_identity") is None)

    receipt["status"] = "PASS" if not receipt.get("fired") else "RED"
    print(json.dumps(receipt, indent=2))
    return 0 if not receipt.get("fired") else 2


if __name__ == "__main__":
    raise SystemExit(main())
