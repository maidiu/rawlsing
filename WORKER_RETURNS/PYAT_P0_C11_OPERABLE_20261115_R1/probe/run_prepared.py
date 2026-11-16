"""Matched cold saved I03: one-session-per-op vs prepared shared session.

TEST_ONLY.  Production files are read-only.  Both modes use the same estate,
catalog, operations, native evaluator and current guard; only session lifetime
and posting-index reuse differ.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from rawlsing_next._pre553_external_i02_certificate import ExternalI02Roots
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission

from court_instrumentation import (
    CourtInstrumentation, cpu_times, current_rss_bytes, directory_bytes,
    process_tree_rss_bytes,
)
from fixture_1006 import ShapeSpec, build_context
from ops import Battery

RESPONDENTS = 128
TAG = "PYAT-COUNTRY-REUSE-20261115"


def jsonable(value):
    return json.loads(canonical_json(value))


def load(receipt):
    ctx = build_context(ShapeSpec(
        "country-reuse", RESPONDENTS, include_weights=True, tag=TAG
    ))
    battery = Battery(ctx)
    ops = battery.build(core_count=80, weighted_count=20)
    catalog = battery.catalog()
    admission = PreparedSavedC11Admission.open(
        root=receipt["root"],
        exact_path=Path(receipt["root"]) / receipt["exact_path"],
        independently_held_manifest_sha256=receipt["manifest_sha256"],
        independently_held_i02=ExternalI02Roots(**receipt["i02"]),
        release_ref=exact_ref(receipt["reconstructed_v1_release_ref"]),
        runtime_catalog=catalog,
        current_authorizer=lambda _roots: True,
    )
    return ops, admission


def fact_record(op, result, wall):
    fact = result.facts[0]
    return {
        "op_id": op.op_id,
        "query_ref": jsonable(op.query_ref),
        "predicate_ref": jsonable(op.predicate_ref),
        "measure": op.measure,
        "core_id": op.core_id,
        "wall_seconds": wall,
        "fact_ref": jsonable(fact.ref),
        "fact_sha256": hashlib.sha256(
            canonical_json(result.facts[0]).encode()
        ).hexdigest(),
        "typed_state": fact.typed_state,
        "raw_numerator_support": fact.raw_numerator_support,
        "raw_denominator_support": fact.raw_denominator_support,
        "weighted_numerator_support": (
            None if getattr(fact, "weighted_numerator_support_if_authorized", None) is None
            else jsonable(fact.weighted_numerator_support_if_authorized)),
        "weighted_denominator_support": (
            None if getattr(fact, "weighted_denominator_support_if_authorized", None) is None
            else jsonable(fact.weighted_denominator_support_if_authorized)),
        "replay_ref": jsonable(fact.replay_ref),
        "release_refs": [jsonable(ref) for ref in result.release_refs],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("baseline", "prepared"), required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    receipt = json.loads((BASE / "evidence" / "estate_receipt.json").read_text())
    ops, admission = load(receipt)
    disk_before = shutil.disk_usage(str(BASE))
    before_cpu = cpu_times()
    before_tree = process_tree_rss_bytes()
    before_rss = current_rss_bytes()
    instrument = CourtInstrumentation()
    rows = []
    start = time.monotonic()
    with instrument.phase(forbid_c11_repository=True) as counters:
        if args.mode == "baseline":
            for op in ops:
                op_start = time.monotonic()
                result = admission.execute_i03(
                    query_ref=op.query_ref, predicate_ref=op.predicate_ref)
                rows.append(fact_record(op, result, time.monotonic() - op_start))
        else:
            with admission.prepared_i03() as prepared:
                for op in ops:
                    op_start = time.monotonic()
                    result = prepared.execute_i03(
                        query_ref=op.query_ref, predicate_ref=op.predicate_ref)
                    rows.append(fact_record(op, result, time.monotonic() - op_start))
                prepared_receipt = prepared.receipt().as_dict()
    wall = time.monotonic() - start
    after_cpu = cpu_times()
    after_tree = process_tree_rss_bytes()
    after_rss = current_rss_bytes()
    disk_after = shutil.disk_usage(str(BASE))
    result = {
        "schema": "PYAT_P0_PREPARED_SAVED_I03@1",
        "mode": args.mode,
        "operations": len(rows),
        "wall_seconds": wall,
        "operations_per_second": len(rows) / wall if wall else None,
        "cpu_user_seconds": after_cpu["user_seconds"] - before_cpu["user_seconds"],
        "cpu_system_seconds": after_cpu["system_seconds"] - before_cpu["system_seconds"],
        "process_tree_rss_before_bytes": before_tree,
        "process_tree_rss_after_bytes": after_tree,
        "process_tree_rss_peak_bytes": max(before_tree, after_tree, after_cpu["maxrss_bytes"]),
        "self_rss_before_bytes": before_rss,
        "self_rss_after_bytes": after_rss,
        "self_maxrss_bytes": after_cpu["maxrss_bytes"],
        "disk_free_before_bytes": disk_before.free,
        "disk_free_after_bytes": disk_after.free,
        "retained_estate_bytes": receipt["retained_bytes"],
        "scratch_dir_bytes_after": directory_bytes(BASE / ".local-data"),
        "counters": counters.material(),
        "prepared_receipt": prepared_receipt if args.mode == "prepared" else None,
        "rows": rows,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "mode": args.mode,
        "operations": len(rows),
        "wall_seconds": wall,
        "ops_per_second": len(rows) / wall if wall else None,
        "session_builds": counters.material()["session_builds"],
        "row_group_reads": counters.material()["row_group_reads"],
        "session_build_seconds": counters.material()["session_build_seconds"],
        "tree_rss_peak_bytes": result["process_tree_rss_peak_bytes"],
        "temp_max_bytes": counters.material()["session_temp_max_bytes"],
        "prepared_receipt": result["prepared_receipt"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
