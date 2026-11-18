#!/usr/bin/env python3
"""One bounded actual-production f4 observation on the sealed R2 estate.

The actual DirectEstateI03Session._respondent_family product method is used;
no test-only adapter/monkeypatch is installed.  Admission and index build are
outside the operation timer; no build/new estate/new pair.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MEASURE = REPO / "WORKER_RETURNS" / "ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117"
sys.path.insert(0, str(MEASURE))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(MEASURE / "vendor"))

import measure_cut1_prepared as harness  # noqa: E402
from court_instrumentation import CourtInstrumentation  # noqa: E402

CONTRACT = MEASURE / "R2_PILOT" / "fixture_contract_pilot.json"
PILOT = MEASURE / "R2_PILOT" / "FIRST_PAIR_RESULT.json"
LABEL = "f4_three_raw"
OUT = HERE / "RESULT.json"


def main() -> int:
    contract, _ctx, bundle, ops = harness.load_contract(CONTRACT)
    estate = contract["estate"]
    by_label = {label: (q, p) for label, q, p in ops}
    query, predicate = by_label[LABEL]
    admission, admission_metrics = harness.admission_open(
        estate, bundle.catalog, lambda _roots: True, prepared=True)
    entry = time.monotonic()
    with admission.prepared_i03() as session:
        index_seconds = time.monotonic() - entry
        instrumentation = CourtInstrumentation()
        with instrumentation.phase(forbid_c11_repository=True) as counters:
            q_start = time.monotonic()
            result = session.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref)
            operation_wall = time.monotonic() - q_start
        serial_start = time.monotonic()
        snapshot = harness.fact_snapshot(result)
        serialization_seconds = time.monotonic() - serial_start
        receipt = session.receipt().as_dict()

    pilot = json.loads(PILOT.read_text())
    baseline = next(
        row for row in pilot["baseline"]["rows"] if row["label"] == LABEL)
    parity_fields = (
        "identity_sha256", "semantic_sha256", "refs_sha256",
        "member_refs_sha256", "replay_sha256")
    parity = {f: snapshot[f] == baseline[f] for f in parity_fields}
    payload = {
        "schema": "ANVIL_PRODUCTION_LOCALITY_QUALIFICATION@1",
        "status": "PRODUCTION_LOCALITY_F4_PARITY" if all(parity.values()) else "PRODUCTION_LOCALITY_PARITY_MISMATCH",
        "product_candidate": "347baec696c8b395d750ac3b9e74417a6490c223",
        "cut1_review": "092bf29ffa6724d477abb4ccfc770e3bc492250d",
        "estate_manifest_sha256": estate["manifest_sha256"],
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "label": LABEL,
        "admission_outside_operation": admission_metrics,
        "index_build_outside_operation_seconds": index_seconds,
        "operation_wall_seconds": operation_wall,
        "serialization_seconds": serialization_seconds,
        "counters": counters.material(),
        "snapshot": snapshot,
        "parity": {"fields": parity, "exact": all(parity.values())},
        "session_receipt": receipt,
        "buffer_limit": "per-respondent/family materialized list; 600 routing facts in sealed f4 witness; no whole-estate corpus",
        "source_pins": {
            "pre553_direct_estate_i03.py_current_blob": "d662fc578a1ecb42d54ec8b4bdab87fd7ecec176",
            "baseline_blob": "8825832f8067c7fce7a99a94505743cbb4eada06",
            "baseline_product": "347baec696c8b395d750ac3b9e74417a6490c223",
            "estate_contract": "e928ebd17016c005efd1c8fee19a19b27e35fb360c6b8f85dd489cc9371b8f28",
        },
        "limitations": [
            "One existing f4 operation on sealed 16R/600Q sourcefree estate; no new build/pair/geometry.",
            "No test-only adapter or monkeypatch is installed.",
            "No native/original35/100k/6GiB/science/actor/CURRENT/production acceptance.",
        ],
    }
    OUT.write_text(json.dumps(harness.plain(payload), indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"], "operation_wall": operation_wall,
        "row_group_reads": counters.material()["row_group_reads"],
        "family_objects": counters.material()["family_object_materializations"],
        "parity": all(parity.values()),
    }, sort_keys=True))
    return 0 if all(parity.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
