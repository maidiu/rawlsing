"""Shared review-only helpers for PYAT1006 independent G5.

Writes only under WORKER_REVIEWS/PYAT1006_PHYSICAL_ECONOMICS_G5_R1/.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import statistics
import sys
import threading
import time
from typing import Any

import psutil

REVIEW = Path(__file__).resolve().parents[1]
REPO = REVIEW.parents[1]
AUTHOR = REPO / "WORKER_RETURNS" / "PYAT1006_PHYSICAL_ECONOMICS_R1"
CAP_BYTES = 6 * 1024 ** 3
MIN_FREE_DISK_BYTES = 3 * 1024 ** 3


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n")


def directory_bytes(path: Path) -> int:
    try:
        return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
    except FileNotFoundError:
        return 0


def disk(path: Path) -> dict[str, int]:
    usage = shutil.disk_usage(path)
    return {"total": usage.total, "used": usage.used, "free": usage.free}


def stats(values: list[float]) -> dict[str, Any]:
    if not values:
        return {"n": 0}
    ordered = sorted(values)

    def pct(percent: float) -> float:
        if len(ordered) == 1:
            return ordered[0]
        position = (len(ordered) - 1) * percent
        low = int(position)
        high = min(low + 1, len(ordered) - 1)
        fraction = position - low
        return ordered[low] * (1 - fraction) + ordered[high] * fraction

    return {
        "n": len(ordered),
        "min": ordered[0],
        "p50": pct(0.50),
        "p95": pct(0.95),
        "max": ordered[-1],
        "mean": statistics.fmean(ordered),
    }


class TreeMonitor:
    """Independent psutil process-tree RSS and disk/staging sampler."""

    def __init__(
        self, pid: int, *, watch: Path, interval: float = 0.25,
        cap_bytes: int = CAP_BYTES,
    ) -> None:
        self.pid = pid
        self.watch = watch
        self.interval = interval
        self.cap_bytes = cap_bytes
        self.peak_tree_rss = 0
        self.peak_own_rss = 0
        self.peak_single_rss = 0
        self.max_processes = 0
        self.samples = 0
        self.peak_root_bytes = 0
        self.peak_stage_bytes = 0
        self.peak_proof_bytes = 0
        self.min_free_disk = disk(watch)["free"]
        self.cap_exceeded = False
        self.started = time.monotonic()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                root = psutil.Process(self.pid)
                processes = [root, *root.children(recursive=True)]
                values = []
                for process in processes:
                    try:
                        values.append(process.memory_info().rss)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                total = sum(values)
                self.samples += 1
                self.max_processes = max(self.max_processes, len(values))
                self.peak_own_rss = max(self.peak_own_rss, values[0] if values else 0)
                self.peak_single_rss = max(self.peak_single_rss, max(values, default=0))
                self.peak_tree_rss = max(self.peak_tree_rss, total)
                if total > self.cap_bytes:
                    self.cap_exceeded = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            try:
                self.peak_root_bytes = max(self.peak_root_bytes, directory_bytes(self.watch))
                for stage in self.watch.glob("**/.s2c-stage-*"):
                    self.peak_stage_bytes = max(
                        self.peak_stage_bytes, directory_bytes(stage)
                    )
                    proof = stage / ".i02-proof.sqlite"
                    if proof.exists():
                        self.peak_proof_bytes = max(
                            self.peak_proof_bytes, proof.stat().st_size
                        )
                self.min_free_disk = min(self.min_free_disk, disk(self.watch)["free"])
            except (FileNotFoundError, OSError):
                pass
            time.sleep(self.interval)

    def __enter__(self) -> "TreeMonitor":
        self._thread.start()
        return self

    def __exit__(self, *_args: Any) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def material(self) -> dict[str, Any]:
        return {
            "tree_peak_rss_bytes": self.peak_tree_rss,
            "own_peak_rss_bytes": self.peak_own_rss,
            "max_single_process_peak_rss_bytes": self.peak_single_rss,
            "max_process_count": self.max_processes,
            "sample_count": self.samples,
            "sampling_interval_seconds": self.interval,
            "cap_bytes": self.cap_bytes,
            "cap_exceeded": self.cap_exceeded,
            "root_peak_bytes": self.peak_root_bytes,
            "stage_peak_bytes": self.peak_stage_bytes,
            "proof_sqlite_peak_bytes": self.peak_proof_bytes,
            "min_free_disk_bytes": self.min_free_disk,
            "elapsed_seconds": time.monotonic() - self.started,
        }


def host_info() -> dict[str, Any]:
    return {
        "hostname": os.uname().nodename,
        "platform": sys.platform,
        "machine": os.uname().machine,
        "mac_ver": os.uname().release,
        "python": sys.version,
        "python_executable": sys.executable,
        "pyarrow": __import__("pyarrow").__version__,
        "psutil": psutil.__version__,
        "cap_bytes": CAP_BYTES,
        "min_free_disk_bytes": MIN_FREE_DISK_BYTES,
    }
