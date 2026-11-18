#!/usr/bin/env python3
"""ONE test-only physical-order query profile on the sealed R2 estate."""
from __future__ import annotations

import cProfile
import hashlib
import io
import json
import pstats
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(ROOT / "vendor"))

import measure_cut1_prepared as harness  # noqa: E402
from court_instrumentation import CourtInstrumentation  # noqa: E402
from rawlsing_next.pre553_prepared_saved_i03 import PreparedI03Session  # noqa: E402
import locality_adapter  # noqa: E402

CONTRACT = ROOT / "R2_PILOT" / "fixture_contract_pilot.json"
PILOT = ROOT / "R2_PILOT" / "FIRST_PAIR_RESULT.json"
R3_RESULT = ROOT / "R3_Q_PROFILE" / "child_result.json"
LABEL = "f4_three_raw"
OUT = HERE / "child_result.json"


def main() -> int:
    contract, ctx, bundle, ops = harness.load_contract(CONTRACT)
    estate = contract["estate"]
    by_label = {label: (q, p) for label, q, p in ops}
    query, predicate = by_label[LABEL]

    admission, h = harness.admission_open(
        estate, bundle.catalog, lambda _roots: True, prepared=True)

    original_family = None
    try:
        original_family = locality_adapter.install()
        entry = time.monotonic()
        with admission.prepared_i03() as session:
            index_build = time.monotonic() - entry
            observed = []
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
    finally:
        if original_family is not None:
            locality_adapter.restore(original_family)

    snapshot = harness.fact_snapshot(result)
    pilot = json.loads(PILOT.read_text())
    baseline_row = next(
        row for row in pilot["baseline"]["rows"] if row["label"] == LABEL)
    parity_fields = (
        "identity_sha256", "semantic_sha256", "refs_sha256",
        "member_refs_sha256", "replay_sha256")
    parity = {f: snapshot[f] == baseline_row[f] for f in parity_fields}
    parity_ok = all(parity.values())
    r3 = json.loads(R3_RESULT.read_text())

    profile.dump_stats(str(HERE / "raw.prof"))
    for name, sort in (("top_cumulative", "cumulative"), ("top_tottime", "tottime")):
        stream = io.StringIO()
        pstats.Stats(profile, stream=stream).sort_stats(sort).print_stats(80)
        (HERE / f"{name}.txt").write_text(stream.getvalue(), encoding="utf-8")
    stream = io.StringIO()
    pstats.Stats(profile, stream=stream).sort_stats("cumulative").print_callers(40)
    (HERE / "callers.txt").write_text(stream.getvalue(), encoding="utf-8")
    stream = io.StringIO()
    pstats.Stats(profile, stream=stream).sort_stats("cumulative").print_stats(20)
    (HERE / "call_tree.txt").write_text(stream.getvalue(), encoding="utf-8")

    payload = {
        "schema": "ANVIL_CUT2_R4_LOCALITY_EXPERIMENT@1",
        "grade": "SOURCEFREE_TEST_ONLY_LOCALITY_EXPERIMENT_NOT_PRODUCTION",
        "product_candidate": "347baec696c8b395d750ac3b9e74417a6490c223",
        "cut1_review": "092bf29ffa6724d477abb4ccfc770e3bc492250d",
        "label": LABEL,
        "estate_manifest_sha256": estate["manifest_sha256"],
        "contract_sha256": hashlib.sha256(CONTRACT.read_bytes()).hexdigest(),
        "changed_mechanism": {
            "file": "pre553_direct_estate_i03.py",
            "symbol": "DirectEstateI03Session._respondent_family",
            "baseline": "SELECT ... ORDER BY ref with one-row-group cache",
            "test_only": "SELECT ... ORDER BY gid,off; then sort materialized objects by ref.key before yield",
            "restoration": "externally observable canonical ref-key order restored before yielding",
            "validation": "same _object_from_row, exact ref/body/respondent/universe checks; no whole-estate materialization",
        },
        "admission_outside_profile": h,
        "index_build_outside_profile_seconds": index_build,
        "profile_query_wall_seconds": q_wall,
        "profile_overhead_disclosure": "same cProfile + CourtInstrumentation settings as R3; not a production timing or speedup.",
        "counters": counters_material,
        "session_receipt": receipt,
        "observer_returned_count": len(observed),
        "snapshot": snapshot,
        "pilot_baseline_identity_sha256": baseline_row["identity_sha256"],
        "parity": {"fields": parity, "exact": parity_ok},
        "r3_baseline_comparator": {
            "profile_query_wall_seconds": r3["profile_query_wall_seconds"],
            "row_group_reads": r3["counters"]["row_group_reads"],
            "row_group_rows": r3["counters"]["row_group_rows"],
            "row_group_compressed_bytes": r3["counters"]["row_group_compressed_bytes"],
            "row_group_uncompressed_bytes": r3["counters"]["row_group_uncompressed_bytes"],
            "family_object_materializations": r3["counters"]["family_object_materializations"],
        },
        "status": "LOCALITY_PROFILE_COMPLETE_PARITY_MATCH" if parity_ok else "LOCALITY_PROFILE_PARITY_MISMATCH",
    }
    OUT.write_text(json.dumps(harness.plain(payload), indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": payload["status"], "q_wall": q_wall,
        "row_group_reads": counters_material["row_group_reads"],
        "row_group_rows": counters_material["row_group_rows"],
        "family_objects": counters_material["family_object_materializations"],
        "parity": parity_ok,
    }, sort_keys=True))
    return 0 if parity_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
