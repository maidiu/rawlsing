#!/usr/bin/env python3
"""One targeted cProfile of actual native execute_i03 on the sealed R2 estate.

Admission and prepared-session/index build are outside the profile.  Exactly one
profiled query execution (f4_three_raw) and one factual parity check occur.
"""
from __future__ import annotations

import cProfile
import hashlib
import io
import json
import pstats
import sys
import time
import traceback
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "vendor"))

import measure_cut1_prepared as harness  # noqa: E402
from court_instrumentation import CourtInstrumentation  # noqa: E402
from rawlsing_next.pre553_prepared_saved_i03 import PreparedI03Session  # noqa: E402

CONTRACT = ROOT / "R2_PILOT" / "fixture_contract_pilot.json"
PILOT = ROOT / "R2_PILOT" / "FIRST_PAIR_RESULT.json"
LABEL = "f4_three_raw"
OUT = HERE / "child_result.json"


def _plain(value: Any) -> Any:
    return harness.plain(value)


def main() -> int:
    contract, ctx, bundle, ops = harness.load_contract(CONTRACT)
    estate = contract["estate"]
    catalog = bundle.catalog
    by_label = {label: (query, predicate) for label, query, predicate in ops}
    query, predicate = by_label[LABEL]

    admission, h = harness.admission_open(
        estate, catalog, lambda _roots: True, prepared=True)

    # Admission is outside the profile; index build is also outside it.
    entry_start = time.monotonic()
    with admission.prepared_i03() as session:
        index_build_seconds = time.monotonic() - entry_start

        # Transparent observer: returns the original object unchanged.
        observed: list[Any] = []
        original_exec = PreparedI03Session.execute_i03

        def observed_exec(self, *args, **kwargs):
            result = original_exec(self, *args, **kwargs)
            observed.append(result)
            return result

        PreparedI03Session.execute_i03 = observed_exec
        profile = cProfile.Profile()
        instrumentation = CourtInstrumentation()
        try:
            with instrumentation.phase(forbid_c11_repository=True) as counters:
                q_start = time.monotonic()
                profile.enable()
                result = session.execute_i03(
                    query_ref=query.ref, predicate_ref=predicate.ref)
                profile.disable()
                q_wall = time.monotonic() - q_start
        finally:
            PreparedI03Session.execute_i03 = original_exec

        counters_material = counters.material()
        receipt = session.receipt().as_dict()

    snapshot = harness.fact_snapshot(result)
    pilot = json.loads(PILOT.read_text())
    baseline_row = next(
        row for row in pilot["baseline"]["rows"] if row["label"] == LABEL)
    parity_fields = (
        "identity_sha256", "semantic_sha256", "refs_sha256",
        "member_refs_sha256", "replay_sha256")
    parity = {field: snapshot[field] == baseline_row[field] for field in parity_fields}
    parity_ok = all(parity.values())

    # Raw pstats and readable views.  Do not strip dirs: source paths are evidence.
    prof_path = HERE / "raw.prof"
    profile.dump_stats(str(prof_path))
    chunks: dict[str, str] = {}
    for name, sort in (("top_cumulative", "cumulative"), ("top_tottime", "tottime")):
        stream = io.StringIO()
        stats = pstats.Stats(profile, stream=stream).sort_stats(sort)
        stats.print_stats(80)
        chunks[name] = stream.getvalue()
        (HERE / f"{name}.txt").write_text(chunks[name], encoding="utf-8")
    stream = io.StringIO()
    pstats.Stats(profile, stream=stream).sort_stats("cumulative").print_callers(40)
    (HERE / "callers.txt").write_text(stream.getvalue(), encoding="utf-8")
    (HERE / "call_tree.txt").write_text(
        chunks["top_cumulative"], encoding="utf-8")

    payload = {
        "schema": "ANVIL_CUT2_R3_Q_PROFILE@1",
        "grade": "SOURCEFREE_TEST_ONLY_PROFILE_NOT_PERFORMANCE_COMPARISON",
        "product_candidate": "347baec696c8b395d750ac3b9e74417a6490c223",
        "cut1_review": "092bf29ffa6724d477abb4ccfc770e3bc492250d",
        "label": LABEL,
        "query_ref": harness.j(query.ref),
        "predicate_ref": harness.j(predicate.ref),
        "estate_manifest_sha256": estate["manifest_sha256"],
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "source_pins": {
            "prepared_module": "rawlsing_next/pre553_prepared_saved_i03.py",
            "prepared_blob": "bcb146edae680028e027e47cae45891693f63526",
            "empirical_query": "rawlsing_next/pre553_empirical_query.py",
            "query_eval": "rawlsing_next/_pre553_query_eval.py",
            "direct_i03": "rawlsing_next/pre553_direct_estate_i03.py",
            "parquet_estate": "rawlsing_next/pre553_source_direct_parquet_estate.py",
            "empirical_objects": "rawlsing_next/pre553_empirical_objects.py",
            "harness": str((ROOT / "measure_cut1_prepared.py").relative_to(ROOT.parent)),
            "harness_sha256": hashlib.sha256(
                (ROOT / "measure_cut1_prepared.py").read_bytes()).hexdigest(),
        },
        "admission_outside_profile": h,
        "index_build_outside_profile_seconds": index_build_seconds,
        "profile_query_wall_seconds": q_wall,
        "profile_overhead_disclosure": "cProfile + CourtInstrumentation wrappers; not a matched timing or speedup.",
        "counters": counters_material,
        "session_receipt": receipt,
        "observer_returned_count": len(observed),
        "snapshot": snapshot,
        "pilot_baseline_identity_sha256": baseline_row["identity_sha256"],
        "parity": {"fields": parity, "exact": parity_ok},
        "profile_files": {
            "raw": "raw.prof",
            "top_cumulative": "top_cumulative.txt",
            "top_tottime": "top_tottime.txt",
            "callers": "callers.txt",
            "call_tree": "call_tree.txt",
        },
        "status": "PROFILE_COMPLETE_PARITY_MATCH" if parity_ok else "PROFILE_PARITY_MISMATCH",
    }
    OUT.write_text(json.dumps(_plain(payload), indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"],
        "label": LABEL,
        "q_wall": q_wall,
        "index_build_outside": index_build_seconds,
        "parity": parity_ok,
        "row_group_reads": counters_material["row_group_reads"],
        "row_group_rows": counters_material["row_group_rows"],
        "profile": str(prof_path),
    }, sort_keys=True))
    return 0 if parity_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
