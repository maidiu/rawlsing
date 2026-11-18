"""Bounded cut1 resource observation over the existing prepared fixture."""
from __future__ import annotations

import json
from pathlib import Path
import resource
import tempfile
import time

import pytest

from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec
from rawlsing_next.pre553_direct_estate_i03 import DirectEstateI03Session
from rawlsing_next.pre553_saved_workload_integration import execute_saved_batch
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture


def main() -> int:
    root = Path(tempfile.mkdtemp(
        prefix="anvil-cut1-resource-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T",
    ))
    mp = pytest.MonkeyPatch()
    try:
        source, qa, predicate, _other, queries, admission = _fixture(
            mp, root / "fixture", "CUT1-RESOURCE")
        units = tuple(
            BatchUnitSpec("QUERY", query.ref, (admission.release_ref,))
            for query in queries.values()
        )
        builds = []
        original_build = DirectEstateI03Session._build

        def counted(self):
            builds.append(1)
            return original_build(self)

        mp.setattr(DirectEstateI03Session, "_build", counted)
        started = time.perf_counter()
        runner = execute_saved_batch(
            admission,
            manifest=BatchManifest(units),
            predicate_ref_by_query={
                query.ref.key: predicate.ref for query in queries.values()
            },
        )
        elapsed = time.perf_counter() - started
        estate_bytes = sum(
            p.stat().st_size for p in Path(admission.estate_path).rglob("*")
            if p.is_file()
        )
        root_bytes = sum(
            p.stat().st_size for p in root.rglob("*") if p.is_file()
        )
        out = {
            "schema": "ANVIL_CUT1_RESOURCE_OBSERVATION@1",
            "fixture": "existing TEST_ONLY prepared sourcefree fixture",
            "respondents": 8,
            "questions": 3,
            "operations": 4,
            "queries": {
                name: query.ref.key for name, query in queries.items()
            },
            "wall_seconds": elapsed,
            "parent_maxrss_bytes": resource.getrusage(
                resource.RUSAGE_SELF).ru_maxrss,
            "process_tree": "single process; no subprocess launched",
            "estate_bytes": estate_bytes,
            "fixture_root_bytes": root_bytes,
            "prepared_index_builds": len(builds),
            "batch_receipts": len(runner.receipts),
            "batch_states": [r.state for r in runner.receipts],
            "output_refs": sum(len(r.result_refs) for r in runner.receipts),
            "source_reads_by_new_batch": 0,
            "full_c11_builds_by_new_batch": 0,
            "limit": "small TEST_ONLY fixture; not original35/100k",
        }
        print(json.dumps(out, indent=2, sort_keys=True))
        return 0
    finally:
        mp.undo()


if __name__ == "__main__":
    raise SystemExit(main())
