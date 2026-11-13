#!/usr/bin/env python3
"""G5 independent probe: Q2 native-fact lineage and optional-weight fate retention.

This does not modify the candidate.  It instruments the existing test helper
`test_pyat960_s1e_native_fact._build_native` and the Q2 handoff to show the
actual dataflow: the claimed native fact builds a *legacy full C11 release* from
a second source decode and uses it as the native repository; the Q2 handoff body
tee is not consumed.  It also compares frontier measure kinds with the returned
operation-fate ledger.

Run on Darwin or Linux:
  PYTHONPATH=. python3 WORKER_RETURNS/PYAT960_S1E_G5/g5_lineage_measure_probe.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import rawlsing_next.pre553_physical_decoder as decoder
import rawlsing_next.tests.test_pyat960_s1e_native_fact as native_fact
from rawlsing_next.tests.test_pyat960_s1e_native_fact import (
    _build_native,
    _native_document,
)
from rawlsing_next.tests.test_pyat960_s1e_support import build, source_fixture


def main() -> int:
    proof = Path(tempfile.mkdtemp(prefix="pyat960-s1e-g5-lineage-"))
    fixture = source_fixture(
        proof / "native", values=(0.0, 1.0, 0.0, 1.0, 0.0))
    document = _native_document(fixture["document"])

    counts = {"snapshot": 0, "sha": 0, "decode_fixture": 0, "legacy_build": 0}
    original_snapshot = decoder._acquire_source_snapshot
    original_sha = decoder._sha
    original_decode_fixture = native_fact.decode_fixture_config
    original_legacy = native_fact.build_validated_c11_release_from_config

    def snapshot(*args, **kwargs):
        counts["snapshot"] += 1
        return original_snapshot(*args, **kwargs)

    def sha(*args, **kwargs):
        counts["sha"] += 1
        return original_sha(*args, **kwargs)

    def decode_fixture(*args, **kwargs):
        counts["decode_fixture"] += 1
        return original_decode_fixture(*args, **kwargs)

    def legacy(*args, **kwargs):
        counts["legacy_build"] += 1
        return original_legacy(*args, **kwargs)

    decoder._acquire_source_snapshot = snapshot
    decoder._sha = sha
    native_fact.decode_fixture_config = decode_fixture
    native_fact.build_validated_c11_release_from_config = legacy
    try:
        handoff, legacy_release, source = _build_native(
            proof / "native", fixture, document, "native.sqlite")
    finally:
        decoder._acquire_source_snapshot = original_snapshot
        decoder._sha = original_sha
        native_fact.decode_fixture_config = original_decode_fixture
        native_fact.build_validated_c11_release_from_config = original_legacy

    frontier = fixture["frontier"]
    fate_rows = list(handoff.operation_fates)
    fate_keys = sorted(fate_rows[0].keys()) if fate_rows else []
    measure_kinds = Counter(op.measure_kind for op in frontier.operations)
    fate_has_measure = any(
        "measure_kind" in row or "measure_id" in row or "weight_ref" in row
        for row in fate_rows)
    predicate_tags = "q2-native"  # _branch_predicate tag in native_fact helper
    operation_ids = {op.op_id for op in frontier.operations}
    query_branch_id = f"BRANCH-{predicate_tags}"
    result = {
        "tested_delivery": "24e6bc02536a0714b0ab94a225f8eef1d84d8127",
        "tested_code_cut": "f6fcd708f8cb8b8fc32bb7f6b9745b3676910be7",
        "source_fixture_bytes": fixture["path"].stat().st_size,
        "frontier_operation_count": len(frontier.operations),
        "frontier_measure_kinds": dict(measure_kinds),
        "handoff_stats": {
            "source_reads": handoff.stats.source_reads,
            "decode_calls": handoff.stats.decode_calls,
            "cell_passes": handoff.stats.cell_passes,
            "full_c11_builds": handoff.stats.full_c11_builds,
        },
        "native_fact_helper_counts": counts,
        "native_fact_total_source_snapshots": counts["snapshot"],
        "native_fact_legacy_full_builds": counts["legacy_build"],
        "handoff_body_transport": handoff.body_transport,
        "native_repository_release_is_legacy": (
            source["release_ref"] == legacy_release.release_ref),
        "legacy_release_ref": legacy_release.release_ref.key,
        "q2_direct_logical_root": handoff.roots.logical,
        "operation_fate_row_keys": fate_keys,
        "operation_fates_preserve_measure_kind": fate_has_measure,
        "issued_receipt_lengths": dict(Counter(
            len(row["issued_receipt_refs"]) for row in fate_rows)),
        "native_first_reader_states": dict(Counter(
            row["native_first_reader_state"] for row in fate_rows)),
        "query_branch_id": query_branch_id,
        "query_branch_is_frontier_operation_id": query_branch_id in operation_ids,
        "operation_ids_sample": sorted(operation_ids)[:3],
        "finding": (
            "The claimed native fact uses a separately built legacy full C11 "
            "release as the body repository (second source decode), not the Q2 "
            "handoff body tee; the Q2 operation fates all carry zero issued "
            "receipt refs and native HOLD. The fate ledger also omits "
            "measure_kind/measure_id/weight_ref, so optional-weight RAW is not "
            "retained in the returned no-drop ledger."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
