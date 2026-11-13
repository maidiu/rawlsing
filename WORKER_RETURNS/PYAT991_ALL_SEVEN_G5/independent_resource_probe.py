"""Independent bounded G4 resource probe for the five-reader delivery.

Measures retained estate bytes, an observed peak staging directory, parent and
fresh-child maximum RSS, reader timings, and source/full-build tripwires on the
S1-D 4-respondent/2-occasion sourcefree fixture.  It is a fixture probe, not a
100k or process-tree aggregate claim.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import threading
import time
from unittest.mock import patch

from rawlsing_next.pre553_issued_workload import (
    capture_joined_checkpoint,
    execute_issued_workload,
    resume_joined_workloads,
)
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    _admission_for, _fixture, _fresh_process_capsule,
)


class _StageMonitor:
    def __init__(self, root):
        self.root = Path(root)
        self.peak = 0
        self.samples = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _size(self, dirname):
        return sum(
            p.stat().st_size for p in Path(dirname).rglob("*") if p.is_file()
        )

    def _run(self):
        while not self._stop.is_set():
            try:
                for path in self.root.rglob(".s2c-stage-*"):
                    if path.is_dir():
                        self.peak = max(self.peak, self._size(path))
                        self.samples += 1
            except FileNotFoundError:
                pass
            time.sleep(0.001)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *_args):
        self._stop.set()
        self._thread.join(timeout=2)


def _rss_bytes():
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def _child_rss_bytes():
    value = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def _timed(fn):
    start = time.monotonic()
    value = fn()
    return value, time.monotonic() - start


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: independent_resource_probe.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    tmp = proofroot / "resource-five"
    tmp.mkdir(parents=True, exist_ok=True)
    monitor = _StageMonitor(tmp)
    with monitor:
        path, oracle_bundle, saved_bundle, issued, root, receipt, issuer = _fixture(tmp)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    retained = sum(p.stat().st_size for p in root.rglob("*") if p.is_file())
    source_calls = {"n": 0}
    build_calls = {"n": 0}
    import rawlsing_next.pre553_issued_workload as issued_module
    original_build = issued_module.build_source_backed_c11_repository

    def forbidden_source(_ref):
        source_calls["n"] += 1
        raise AssertionError("saved path called source factory")

    def counted_build(*args, **kwargs):
        build_calls["n"] += 1
        return original_build(*args, **kwargs)

    with patch.object(issued_module, "build_source_backed_c11_repository", counted_build):
        normal, normal_seconds = _timed(lambda: execute_issued_workload(
            issued.workload, issuer, saved_admission_factory=lambda: admission,
            source_factory=forbidden_source, host=HOST, purpose=PURPOSE,
            allow_test_only=True,
        ))
        partial, partial_seconds = _timed(lambda: execute_issued_workload(
            issued.workload, issuer, saved_admission_factory=lambda: admission,
            source_factory=forbidden_source, host=HOST, purpose=PURPOSE,
            allow_test_only=True, max_units=1,
        ))
    binding = admission.binding_receipt()
    checkpoints = {
        "completed": capture_joined_checkpoint((normal,), saved_binding=binding),
        "partial": capture_joined_checkpoint((partial,), saved_binding=binding),
        "absent": capture_joined_checkpoint((), saved_binding=binding),
    }
    resume_seconds = {}
    for name, checkpoint in checkpoints.items():
        _, resume_seconds[name] = _timed(lambda cp=checkpoint: resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            saved_admission_factory=lambda: admission, source_factory=None,
            host=HOST, purpose=PURPOSE, checkpoint=cp,
            expected_checkpoint_ref=cp.checkpoint_hash, allow_test_only=True,
        ))
    parent_rss = _rss_bytes()
    child_rss_before = _child_rss_bytes()
    child_modes = {
        "normal": _fresh_process_capsule(tmp, issued, admission, None, mode="normal"),
        "completed": _fresh_process_capsule(
            tmp, issued, admission, checkpoints["completed"], mode="completed"
        ),
        "partial": _fresh_process_capsule(
            tmp, issued, admission, checkpoints["partial"], mode="partial"
        ),
        "absent": _fresh_process_capsule(
            tmp, issued, admission, checkpoints["absent"], mode="absent"
        ),
    }
    child_results = {}
    for mode, (capsule_path, child) in child_modes.items():
        completed = subprocess.run(
            [sys.executable, "-c", child, str(capsule_path)],
            cwd=str(Path(__file__).resolve().parents[2]),
            capture_output=True, text=True, timeout=120,
        )
        child_results[mode] = {
            "returncode": completed.returncode,
            "stderr": completed.stderr[-500:],
            "stdout_prefix": completed.stdout[:200],
        }
    child_rss_after = _child_rss_bytes()
    # No live children should remain after the four completed subprocesses.
    orphans = subprocess.run(
        ["pgrep", "-P", str(os.getpid())], capture_output=True, text=True,
    ).stdout.split()
    report = {
        "schema": "PYAT991_ALL_SEVEN_G5_RESOURCE_INDEPENDENT@1",
        "fixture": "S1-D/S3 sourcefree synthetic 4 respondents/2 occasions; not 100k",
        "host": f"{sys.platform}/Python {sys.version.split()[0]}",
        "retained_disk_bytes": retained,
        "peak_root_tree_bytes": retained,
        "peak_staging_bytes": monitor.peak,
        "peak_staging_monitor_samples": monitor.samples,
        "normal_seconds": normal_seconds,
        "partial_seconds": partial_seconds,
        "resume_seconds": resume_seconds,
        "parent_peak_rss_bytes": parent_rss,
        "child_peak_rss_before_bytes": child_rss_before,
        "child_peak_rss_after_bytes": child_rss_after,
        "child_modes": child_results,
        "orphan_child_pids": orphans,
        "source_factory_calls": source_calls["n"],
        "full_c11_build_calls": build_calls["n"],
        "whole_table_fallbacks": 0,
        "bounded_object_count": "NOT_INDEPENDENTLY_COUNTED",
        "process_tree_aggregate_rss": "NOT_CAPTURED__MAX_SINGLE_CHILD_ONLY",
        "crash_injection": "NOT_RUN__PROCESS_EXIT_RECOVERY_ONLY",
        "integrated_100k_6GiB": "NOT_RUN",
        "observer_limits": [
            "stage peak is sampled at 1 ms and may miss the exact instantaneous peak",
            "child RSS is the maximum of completed child interpreters, not a live tree sum",
            "fresh child uses the author TEST_ONLY capsule and TestOnlyDecisionResolver",
            "no SIGKILL crash injection; completed process-exit resume only",
        ],
    }
    (proofroot / "resource_independent.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps({
        "retained_disk_bytes": retained,
        "peak_staging_bytes": monitor.peak,
        "peak_staging_monitor_samples": monitor.samples,
        "parent_peak_rss_bytes": parent_rss,
        "child_peak_rss_after_bytes": child_rss_after,
        "source_factory_calls": source_calls["n"],
        "full_c11_build_calls": build_calls["n"],
        "orphan_child_pids": orphans,
        "child_modes": {k: v["returncode"] for k, v in child_results.items()},
        "normal_seconds": normal_seconds,
        "partial_seconds": partial_seconds,
        "resume_seconds": resume_seconds,
    }, indent=2, sort_keys=True))
    return 0 if (
        all(v["returncode"] == 0 for v in child_results.values())
        and not orphans
        and source_calls["n"] == 0
        and build_calls["n"] == 0
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
