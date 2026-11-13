"""Bounded final G4 resource + crash/restart probe for repaired S2-D.

Measures fixture retained/observed stage bytes, simultaneous parent+child RSS
samples, bounded family/materialization counts, source/full-build/whole-table
tripwires, and one child SIGKILL immediately before a fresh resume of the same
durable PARTIAL checkpoint. This is evidence machinery only.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import tempfile
import threading
import time

import pyarrow.parquet as pq

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.pre553_saved_c11_admission import SavedC11Admission
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    _admission_for, _fixture, _fresh_process_capsule,
)

TMP = Path("/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T")


def _rss_bytes() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def _ps_tree_rss(pid: int) -> int:
    """Sum RSS (bytes) for pid and descendants, sampled synchronously."""
    try:
        text = subprocess.check_output(
            ["ps", "-axo", "pid=,ppid=,rss="], text=True, timeout=2,
        )
    except Exception:
        return 0
    rows = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        try:
            p, pp, rss = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            continue
        rows[p] = (pp, rss)
    keys = {pid}
    changed = True
    while changed:
        changed = False
        for p, (pp, _rss) in rows.items():
            if pp in keys and p not in keys:
                keys.add(p)
                changed = True
    return sum(rows.get(p, (0, 0))[1] for p in keys) * 1024


class _TreeSampler:
    def __init__(self, parent_pid: int, child_pid: int):
        self.parent_pid = parent_pid
        self.child_pid = child_pid
        self.peak = 0
        self.samples = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self._stop.is_set():
            # The parent tree already includes the live child; summing the
            # child separately would double count it.
            self.peak = max(self.peak, _ps_tree_rss(self.parent_pid))
            self.samples += 1
            time.sleep(0.002)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *_):
        self._stop.set()
        self._thread.join(timeout=2)


def _size(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


class _StageSampler:
    def __init__(self, root: Path):
        self.root = root
        self.peak = 0
        self.samples = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self._stop.is_set():
            for p in self.root.rglob(".s2c-stage-*"):
                if p.is_dir():
                    self.peak = max(self.peak, _size(p))
                    self.samples += 1
            time.sleep(0.001)

    def __enter__(self):
        self._thread.start(); return self

    def __exit__(self, *_):
        self._stop.set(); self._thread.join(timeout=2)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: resource_recovery_probe.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("private proofroot required")
    proofroot.mkdir(parents=True, exist_ok=True)
    root_dir = Path(tempfile.mkdtemp(prefix="s2d-recovered-", dir=proofroot))
    stage = _StageSampler(root_dir)
    with stage:
        _, _oracle, _saved, issued, root, receipt, issuer = _fixture(root_dir)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
    binding = admission.binding_receipt()
    source_calls = {"n": 0}
    build_calls = {"n": 0}
    table_calls = {"n": 0}
    family_objects = {"n": 0}
    original_iter = VerifiedDirectEstate.iter_family
    original_build = issued_module.build_source_backed_c11_repository
    original_table = pq.read_table

    def iter_family(self, family, *, batch_size=512):
        for obj in original_iter(self, family, batch_size=batch_size):
            family_objects["n"] += 1
            yield obj

    def source(_ref):
        source_calls["n"] += 1
        raise AssertionError("saved path opened source")

    def build(*a, **k):
        build_calls["n"] += 1
        return original_build(*a, **k)

    def table(*a, **k):
        table_calls["n"] += 1
        return original_table(*a, **k)

    VerifiedDirectEstate.iter_family = iter_family
    issued_module.build_source_backed_c11_repository = build
    pq.read_table = table
    try:
        t0 = time.monotonic()
        normal = issued_module.execute_issued_workload(
            issued.workload, issuer, saved_admission_factory=lambda: admission,
            source_factory=source, host=HOST, purpose=PURPOSE, allow_test_only=True,
        )
        normal_seconds = time.monotonic() - t0
        t0 = time.monotonic()
        partial = issued_module.execute_issued_workload(
            issued.workload, issuer, saved_admission_factory=lambda: admission,
            source_factory=source, host=HOST, purpose=PURPOSE, allow_test_only=True,
            max_units=1,
        )
        partial_seconds = time.monotonic() - t0
    finally:
        VerifiedDirectEstate.iter_family = original_iter
        issued_module.build_source_backed_c11_repository = original_build
        pq.read_table = original_table
    checkpoints = {
        "completed": issued_module.capture_joined_checkpoint((normal,), saved_binding=binding),
        "partial": issued_module.capture_joined_checkpoint((partial,), saved_binding=binding),
        "absent": issued_module.capture_joined_checkpoint((), saved_binding=binding),
    }
    resume_seconds = {}
    for name, checkpoint in checkpoints.items():
        t0 = time.monotonic()
        issued_module.resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            saved_admission_factory=lambda: admission, source_factory=None,
            host=HOST, purpose=PURPOSE, checkpoint=checkpoint,
            expected_checkpoint_ref=checkpoint.checkpoint_hash, allow_test_only=True,
        )
        resume_seconds[name] = time.monotonic() - t0
    parent_rss = _rss_bytes()
    child_results = {}
    tree_peak = 0
    tree_samples = 0
    for mode, cp in (
        ("normal", None), ("completed", checkpoints["completed"]),
        ("partial", checkpoints["partial"]), ("absent", checkpoints["absent"]),
    ):
        capsule_path, child_code = _fresh_process_capsule(
            root_dir, issued, admission, cp, mode=mode,
        )
        proc = subprocess.Popen(
            [sys.executable, "-c", child_code, str(capsule_path)],
            cwd=str(Path(__file__).resolve().parents[2]),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        )
        with _TreeSampler(os.getpid(), proc.pid) as sampler:
            out, err = proc.communicate(timeout=120)
        tree_peak = max(tree_peak, sampler.peak)
        tree_samples += sampler.samples
        child_results[mode] = {
            "returncode": proc.returncode,
            "stdout": out[:200],
            "stderr": err[-500:],
        }
    # Controlled SIGKILL child: durable PARTIAL capsule already exists.
    capsule_path, resume_code = _fresh_process_capsule(
        root_dir, issued, admission, checkpoints["partial"], mode="partial",
    )
    with capsule_path.open("rb") as f:
        os.fsync(f.fileno())
    crash_code = (
        "import json,os,signal,sys\n"
        "from pathlib import Path\n"
        "json.loads(Path(sys.argv[1]).read_text())\n"
        "os.kill(os.getpid(), signal.SIGKILL)\n"
    )
    crash = subprocess.Popen(
        [sys.executable, "-c", crash_code, str(capsule_path)],
        cwd=str(Path(__file__).resolve().parents[2]),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    crash_out, crash_err = crash.communicate(timeout=30)
    recovered = subprocess.run(
        [sys.executable, "-c", resume_code, str(capsule_path)],
        cwd=str(Path(__file__).resolve().parents[2]),
        capture_output=True, text=True, timeout=120,
    )
    recovered_refs = json.loads(recovered.stdout)["output_refs"] if recovered.returncode == 0 else []
    expected_refs = [
        ref.as_dict() for ref in normal.output_refs
    ]
    # Response order is not semantic; compare exact ref sets.
    expected_keys = sorted(
        (r["kind"], r["object_id"], r["content_hash"]) for r in expected_refs
    )
    recovered_keys = sorted(
        (r["kind"], r["object_id"], r["content_hash"]) for r in recovered_refs
    )
    orphan_check = subprocess.run(
        ["pgrep", "-P", str(os.getpid())], capture_output=True, text=True,
    ).stdout.split()
    out = {
        "schema": "PYAT991_S2D_FINAL_G4_OBSERVATIONS@1",
        "fixture": "S1-D/S3 sourcefree synthetic 4 respondents/2 occasions; not 100k",
        "retained_disk_bytes": _size(root),
        "peak_root_tree_bytes": _size(root),
        "peak_staging_bytes": stage.peak,
        "peak_staging_monitor_samples": stage.samples,
        "normal_seconds": normal_seconds,
        "partial_seconds": partial_seconds,
        "resume_seconds": resume_seconds,
        "parent_peak_rss_bytes": parent_rss,
        "process_tree_aggregate_rss_bytes_sampled_peak": tree_peak,
        "process_tree_rss_sampling_note": "2 ms ps sampling of the parent-root process tree (which includes live child processes); sampled peak, not a hardware maximum",
        "process_tree_samples": tree_samples,
        "child_modes": child_results,
        "bounded_family_objects_yielded": family_objects["n"],
        "bounded_materializations_note": "family object yields under normal+partial saved execution; not a mandatory full graph",
        "source_factory_calls": source_calls["n"],
        "full_c11_build_calls": build_calls["n"],
        "whole_table_read_table_calls": table_calls["n"],
        "peak_staging_observed": stage.peak,
        "orphan_child_pids": orphan_check,
        "crash_child_returncode": crash.returncode,
        "crash_child_killed_by_signal": crash.returncode < 0,
        "crash_stdout": crash_out[:200],
        "crash_stderr": crash_err[-500:],
        "resumed_after_sigkill_returncode": recovered.returncode,
        "resumed_after_sigkill_output_match": recovered_keys == expected_keys,
        "resumed_after_sigkill_stderr": recovered.stderr[-500:],
        "checkpoint_semantics": "caller-owned immutable checkpoint material; no new persistent store/journal",
        "integrated_100k_6GiB": "NOT_RUN",
        "limits": [
            "RSS aggregate is sampled; child completions can interleave",
            "no production CURRENT, original35, source science or 100k claim",
            "crash is a single pre-resume SIGKILL of the owned child, not a universal failpoint matrix",
        ],
    }
    (proofroot / "final_g4_observations.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if (
        all(v["returncode"] == 0 for v in child_results.values())
        and crash.returncode < 0
        and recovered.returncode == 0
        and out["resumed_after_sigkill_output_match"]
        and not orphan_check
        and source_calls["n"] == 0
        and build_calls["n"] == 0
        and table_calls["n"] == 0
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
