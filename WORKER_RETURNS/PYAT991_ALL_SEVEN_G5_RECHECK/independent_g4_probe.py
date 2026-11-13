"""Independent bounded G4 probe on the fixed PARTIAL-repair cut.

Covers fixed-fixture retained/stage bytes, sampled parent-root process-tree RSS
during each fresh child mode (normal/completed/partial/absent), a separate
fresh-Batch tree sample, parent normal/partial source/build/table/family
tripwires, scratch/orphan checks, and timing.  It is not a 100k or production
resource claim.
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

import pyarrow.parquet as pq

import rawlsing_next.pre553_issued_workload as issued_module
from rawlsing_next.pre553_source_direct_parquet_estate import VerifiedDirectEstate
from rawlsing_next.tests.test_pyat940_s1d_current_permissions import HOST, PURPOSE
from rawlsing_next.tests.test_pyat991_s2d_five_readers import (
    _admission_for, _fixture, _fresh_process_capsule,
)


def _rss_bytes(value):
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def _ps_tree_rss(pid):
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
    def __init__(self, root_pid):
        self.root_pid = root_pid
        self.peak = 0
        self.samples = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self._stop.is_set():
            self.peak = max(self.peak, _ps_tree_rss(self.root_pid))
            self.samples += 1
            time.sleep(0.002)

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, *_args):
        self._stop.set()
        self._thread.join(timeout=2)


class _StageSampler:
    def __init__(self, root):
        self.root = Path(root)
        self.peak = 0
        self.samples = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _size(self, directory):
        return sum(p.stat().st_size for p in Path(directory).rglob("*") if p.is_file())

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


def _timed(fn):
    start = time.monotonic()
    value = fn()
    return value, time.monotonic() - start


def _run_child(capsule_path, child, timeout=120):
    proc = subprocess.Popen(
        [sys.executable, "-c", child, str(capsule_path)],
        cwd=str(Path(__file__).resolve().parents[2]),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    sampler = _TreeSampler(os.getpid())
    with sampler:
        out, err = proc.communicate(timeout=timeout)
    return proc, out, err, sampler.peak, sampler.samples


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: independent_g4_probe.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    if not str(proofroot).startswith("/private/var/folders/"):
        raise SystemExit("proofroot must be the approved private temp path")
    tmp = proofroot / "g4-independent"
    tmp.mkdir(parents=True, exist_ok=True)
    stage = _StageSampler(tmp)
    with stage:
        _, _, _, issued, root, receipt, issuer = _fixture(tmp)
    admission = _admission_for(
        root, receipt, issued.workload,
        lambda _roots: issuer.resolve_current(issued.record.decision_ref) == issued.record,
    )
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

    def build(*args, **kwargs):
        build_calls["n"] += 1
        return original_build(*args, **kwargs)

    def table(*args, **kwargs):
        table_calls["n"] += 1
        return original_table(*args, **kwargs)

    VerifiedDirectEstate.iter_family = iter_family
    issued_module.build_source_backed_c11_repository = build
    pq.read_table = table
    try:
        normal, normal_seconds = _timed(lambda: issued_module.execute_issued_workload(
            issued.workload, issuer, saved_admission_factory=lambda: admission,
            source_factory=source, host=HOST, purpose=PURPOSE, allow_test_only=True,
        ))
        partial, partial_seconds = _timed(lambda: issued_module.execute_issued_workload(
            issued.workload, issuer, saved_admission_factory=lambda: admission,
            source_factory=source, host=HOST, purpose=PURPOSE, allow_test_only=True,
            max_units=1,
        ))
    finally:
        VerifiedDirectEstate.iter_family = original_iter
        issued_module.build_source_backed_c11_repository = original_build
        pq.read_table = original_table
    binding = admission.binding_receipt()
    checkpoints = {
        "completed": issued_module.capture_joined_checkpoint((normal,), saved_binding=binding),
        "partial": issued_module.capture_joined_checkpoint((partial,), saved_binding=binding),
        "absent": issued_module.capture_joined_checkpoint((), saved_binding=binding),
    }
    resume_seconds = {}
    for name, checkpoint in checkpoints.items():
        _, resume_seconds[name] = _timed(lambda cp=checkpoint: issued_module.resume_joined_workloads(
            workloads=(issued,), resolver=issuer,
            saved_admission_factory=lambda: admission, source_factory=None,
            host=HOST, purpose=PURPOSE, checkpoint=cp,
            expected_checkpoint_ref=cp.checkpoint_hash, allow_test_only=True,
        ))
    expected_refs = sorted(ref.key for ref in normal.output_refs)
    child_results = {}
    for mode, checkpoint in (
        ("normal", None), ("completed", checkpoints["completed"]),
        ("partial", checkpoints["partial"]), ("absent", checkpoints["absent"]),
    ):
        capsule_path, child = _fresh_process_capsule(
            tmp, issued, admission, checkpoint, mode=mode,
        )
        proc, out, err, peak, samples = _run_child(capsule_path, child)
        try:
            observed_refs = sorted(
                (ref["kind"], ref["object_id"], ref["content_hash"])
                for ref in json.loads(out)["output_refs"]
            )
        except Exception:
            observed_refs = []
        child_results[mode] = {
            "returncode": proc.returncode,
            "stderr": err[-300:],
            "process_tree_peak_rss_bytes": peak,
            "process_tree_samples": samples,
            "output_refs_equal_normal": observed_refs == sorted(
                (ref.kind, ref.object_id, ref.content_hash) for ref in normal.output_refs
            ),
        }
    # Independent fresh Batch child, sampled as its own parent-root tree.
    batch_script = Path(__file__).resolve().parents[2] / "WORKER_RETURNS/PYAT991_ALL_SEVEN_G5/independent_fresh_batch.py"
    batch_dir = proofroot / "batch-probe"
    if batch_dir.exists():
        import shutil
        for p in batch_dir.glob("fresh-batch"):
            shutil.rmtree(p, ignore_errors=True)
    batch = subprocess.Popen(
        [sys.executable, str(batch_script), str(batch_dir)],
        cwd=str(Path(__file__).resolve().parents[2]),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    batch_sampler = _TreeSampler(os.getpid())
    with batch_sampler:
        batch_out, batch_err = batch.communicate(timeout=180)
    retained = sum(p.stat().st_size for p in root.rglob("*") if p.is_file())
    scratch = [str(p) for p in root.rglob("*") if p.name.startswith(".s2c-stage-") or p.name == ".i02-proof.sqlite"]
    orphans = subprocess.run(["pgrep", "-P", str(os.getpid())], capture_output=True, text=True).stdout.split()
    out = {
        "schema": "PYAT991_ALL_SEVEN_G5_G4_INDEPENDENT@1",
        "fixture": "S1-D/S3 sourcefree synthetic 4 respondents/2 occasions; not 100k",
        "host": f"{sys.platform}/Python {sys.version.split()[0]}",
        "retained_disk_bytes": retained,
        "peak_root_tree_bytes": retained,
        "peak_staging_bytes": stage.peak,
        "peak_staging_samples": stage.samples,
        "parent_peak_rss_bytes": _rss_bytes(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),
        "normal_seconds": normal_seconds,
        "partial_seconds": partial_seconds,
        "resume_seconds": resume_seconds,
        "normal_output_refs": len(normal.output_refs),
        "partial_output_refs": len(partial.output_refs),
        "source_factory_calls_parent_normal_partial": source_calls["n"],
        "full_c11_build_calls_parent_normal_partial": build_calls["n"],
        "whole_table_read_table_calls_parent_normal_partial": table_calls["n"],
        "bounded_family_objects_yielded_parent_normal_partial": family_objects["n"],
        "counter_coverage": "parent normal+partial only; fresh child modes are not included in family/source/build counters",
        "child_results": child_results,
        "fresh_batch_probe": {
            "returncode": batch.returncode,
            "stderr": batch_err[-300:],
            "stdout": batch_out[:300],
            "process_tree_peak_rss_bytes": batch_sampler.peak,
            "process_tree_samples": batch_sampler.samples,
        },
        "scratch_leftovers": scratch,
        "orphan_child_pids": orphans,
        "crash_witness": "SEPARATE_OWN_NATIVE_BOUNDARY_WITNESS__see_native_crash_witness.json",
        "process_tree_aggregate_scope": "sampled parent-root tree including live descendants; max is not exact hardware maximum",
        "integrated_100k_6GiB": "NOT_RUN",
        "new_modules_linux": "NOT_RUN; Darwin-only",
    }
    (proofroot / "g4_independent.json").write_text(
        json.dumps(out, indent=2, sort_keys=True), encoding="utf-8",
    )
    print(json.dumps({
        "retained_disk_bytes": retained,
        "peak_staging_bytes": stage.peak,
        "parent_peak_rss_bytes": out["parent_peak_rss_bytes"],
        "child_modes": {
            k: {
                "returncode": v["returncode"],
                "tree_peak": v["process_tree_peak_rss_bytes"],
                "outputs_equal": v["output_refs_equal_normal"],
            } for k, v in child_results.items()
        },
        "fresh_batch": {
            "returncode": batch.returncode,
            "tree_peak": batch_sampler.peak,
            "outputs": batch_out[:120],
        },
        "source_build_table_calls": [source_calls["n"], build_calls["n"], table_calls["n"]],
        "family_objects": family_objects["n"],
        "scratch_leftovers": scratch,
        "orphans": orphans,
    }, indent=2, sort_keys=True))
    return 0 if (
        all(v["returncode"] == 0 and v["output_refs_equal_normal"] for v in child_results.values())
        and batch.returncode == 0
        and source_calls["n"] == build_calls["n"] == table_calls["n"] == 0
        and not scratch and not orphans
    ) else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
