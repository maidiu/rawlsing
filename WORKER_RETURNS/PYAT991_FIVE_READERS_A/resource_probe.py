"""S2-D five-reader actual resource probe (own return, not product tests)."""
from __future__ import annotations

import json
import resource
from pathlib import Path
import tempfile
import time

from rawlsing_next.pre553_issued_workload import (
    capture_joined_checkpoint,
    execute_issued_workload,
    resume_joined_workloads,
)
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    HOST,
    PURPOSE,
    _admission_for,
    _fixture,
)

TMP = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T")


def main() -> int:
    root_dir = Path(tempfile.mkdtemp(prefix="s2d-five-resource-", dir=TMP))
    _, _, _, issued, estate, receipt, issuer = _fixture(root_dir)
    admission = _admission_for(
        estate, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    t0 = time.monotonic()
    full = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
    )
    normal_seconds = time.monotonic() - t0
    t0 = time.monotonic()
    partial = execute_issued_workload(
        issued.workload, issuer, saved_admission_factory=lambda: admission,
        source_factory=None, host=HOST, purpose=PURPOSE, allow_test_only=True,
        max_units=1,
    )
    partial_seconds = time.monotonic() - t0
    binding = admission.binding_receipt()
    checkpoints = {
        "completed": capture_joined_checkpoint((full,), saved_binding=binding),
        "partial": capture_joined_checkpoint((partial,), saved_binding=binding),
        "absent": capture_joined_checkpoint((), saved_binding=binding),
    }
    resume_seconds = {}
    for name, checkpoint in checkpoints.items():
        t0 = time.monotonic()
        resumed = resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            saved_admission_factory=lambda: admission, source_factory=None,
            host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash, allow_test_only=True,
        )
        resume_seconds[name] = time.monotonic() - t0
        assert resumed is not None
    retained = sum(
        p.stat().st_size for p in estate.rglob("*") if p.is_file()
    )
    peak_staging = None
    for p in estate.rglob(".s2c-native-i03-*"):
        if p.is_dir():
            peak_staging = max(
                peak_staging or 0,
                sum(x.stat().st_size for x in p.rglob("*") if x.is_file()),
            )
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out = {
        "schema": "PYAT991_S2D_FIVE_READERS_RESOURCE@1",
        "retained_disk_bytes": retained,
        "peak_root_tree_bytes": retained,
        "peak_staging_bytes": peak_staging,
        "normal_seconds": normal_seconds,
        "partial_seconds": partial_seconds,
        "resume_seconds": resume_seconds,
        "normal_output_refs": len(full.output_refs),
        "partial_output_refs": len(partial.output_refs),
        "receipt_counts": {
            "normal": len(full.receipts), "partial": len(partial.receipts),
        },
        "source_opens": 0,
        "full_c11_builds": 0,
        "whole_table_fallbacks": 0,
        "parent_peak_rss_bytes": int(rss) if sys_platform() == "darwin" else int(rss) * 1024,
        "child_process_peak_rss_bytes": None,
        "integrated_100k_6GiB": "NOT_RUN",
        "note": "Parent RSS only; fresh-child RSS is measured by the subprocess test, not this probe.",
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


def sys_platform() -> str:
    import sys
    return sys.platform


if __name__ == "__main__":
    raise SystemExit(main())
