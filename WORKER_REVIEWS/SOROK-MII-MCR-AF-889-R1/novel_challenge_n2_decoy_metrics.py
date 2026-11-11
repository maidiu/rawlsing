#!/usr/bin/env python3
"""Reviewer-owned novel challenge N2 (corrected) — verifier-enforced rejection.

The first N2 revision only showed that invented metrics had no observed
producer; that is reviewer-side detection, not proof that the real receiving
predicate rejects a mixed forged receipt. This revision executes the actual
acceptance predicate `assess_receipts` from `mcr_full_e1_e10_gate.py` against:

  * a genuine independently observed `run_p6.experience` digest (real call,
    reviewer profiler), used by the valid outcomes, and
  * three fabricated E3/E8/E9 outcome records whose measurement values
    (exposure-ledger writes, replay failures, p95/cold-start latency) were
    never produced by that call, with digests derived from the fabrication.

It then requires `assess_receipts` to raise RED naming the fabricated outcome,
and requires the all-genuine control receipt to pass. A real call is necessary
but never sufficient; the verifier must enforce per-outcome observer binding.

Run: python3 -B novel_challenge_n2_decoy_metrics.py
Requires MCR_QUALIFIED_RUNTIME_ROOT / MCR_QUALIFIED_RUNTIME_SHA like the
author consumer trace (separately authenticated protected checkout).
"""
import argparse
import hashlib
import importlib
import importlib.util
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
COMM = ROOT / "WORKER_COMMISSIONS/SOROK-MECHANISM-II-HISTORICALLY-MEDIATED-GAZE-20261108-R1"
GATE_PATH = COMM / "mcr_full_e1_e10_gate.py"
MATRIX_PATH = COMM / "mcr_full_e1_e10_acceptance.json"


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


def real_p6_call(state, command, **kw):
    run_p6 = importlib.import_module("run_p6")
    args = argparse.Namespace(command=command, request_id=None, **kw)
    return run_p6.experience(state, args, provider_mode="INJECTED")


def load_gate():
    spec = importlib.util.spec_from_file_location("mcr_full_e1_e10_gate", GATE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    receipt = {"probe": "N2-VERIFIER-ENFORCED-MIXED-FORGERY", "checks": []}

    def check(name, ok, detail=""):
        receipt["checks"].append({"name": name, "result": "PASS" if ok else "RED",
                                  "detail": detail})
        if not ok:
            receipt.setdefault("fired", []).append(name)

    authenticate()
    gate = load_gate()
    ids = gate.matrix()
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    package = {row["id"]: row["package"] for row in matrix["records"]}

    with tempfile.TemporaryDirectory(prefix="mcr-n2g-") as td:
        state = Path(td) / "world"
        real_p6_call(state, "new", situated_house=True)
        observed = real_p6_call(state, "view")
    genuine_digest = digest(observed)
    check("genuine_p6_return_observed",
          isinstance(observed, dict) and bool(genuine_digest),
          f"digest={genuine_digest[:16]}…")

    forged_packages = ("MII-E03", "MII-E08", "MII-E09")
    fabricated = {"e3_exposure_ledger_writes": 2, "e8_replay_failures": 0,
                  "e9_latency_p95_ms": 3, "e9_cold_start_ms": 41}
    fabricated_digest = digest(fabricated)
    witness = {f"MII-E{i:02d}": genuine_digest for i in range(1, 11)}

    def record(oid, forged):
        rec = {"id": oid, "package": package[oid], "status": "PASS",
               "grade": "SOURCEFREE_S2",
               "independent_actual_source_witness": {"actual_source_calls": [
                   {"module": "run_p6", "function": "experience", "event": "return"}]},
               "qualified_source_denial": True, "exact_source_restore": True,
               "actual_first_reader_output_sha256":
                   fabricated_digest if forged else genuine_digest,
               "reviewer_command":
                   "python3 -B independent_full_e1_e10_suite.py --observed-only",
               "reviewer_command_origin": "INDEPENDENT_NONAUTHOR_SOURCE"}
        if forged:
            rec.update(fabricated)
        return rec

    control = [record(oid, False) for oid in ids]
    mixed = [record(oid, package[oid] in forged_packages) for oid in ids]

    control_ok = True
    try:
        control_ok = gate.assess_receipts(ids, control, witnesses=witness) is True
    except RuntimeError as exc:
        control_ok = False
        receipt["control_error"] = str(exc)
    check("all_genuine_control_accepted_by_predicate", control_ok)

    rejected = None
    try:
        gate.assess_receipts(ids, mixed, witnesses=witness)
    except RuntimeError as exc:
        rejected = str(exc)
    check("mixed_genuine_digest_plus_fabricated_e3_e8_e9_rejected",
          bool(rejected) and rejected.startswith(
              "MCR_MISSION_TEST_RETURNS_DIFFER_FROM_RECEIVER_OBSERVED_P6_"),
          rejected or "predicate accepted the mixed forged receipt")
    forged_id = next((oid for oid in ids if package[oid] in forged_packages), None)
    check("rejection_names_fabricated_outcome",
          bool(rejected) and forged_id is not None and rejected.endswith(forged_id),
          f"expected suffix {forged_id}")

    receipt["status"] = "PASS" if not receipt.get("fired") else "RED"
    receipt["forged_packages"] = list(forged_packages)
    receipt["forged_ids"] = [oid for oid in ids if package[oid] in forged_packages]
    receipt["genuine_digest_sha256"] = genuine_digest
    receipt["fabricated_digest_sha256"] = fabricated_digest
    print(json.dumps(receipt, indent=2))
    return 0 if not receipt.get("fired") else 2


if __name__ == "__main__":
    raise SystemExit(main())
