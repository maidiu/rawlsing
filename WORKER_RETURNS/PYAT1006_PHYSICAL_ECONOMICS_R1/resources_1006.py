"""Process-tree RSS, disk reserve and host-capacity measurement for #1006."""
from __future__ import annotations

from dataclasses import dataclass, field
import os
from pathlib import Path
import platform
import resource
import shutil
import signal
import subprocess
import sys
import threading
import time
from typing import Any

import psutil


CAP_BYTES = 6 * 1024 ** 3
MIN_FREE_DISK_BYTES = 3 * 1024 ** 3


def rss_self_bytes() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def rss_children_bytes() -> int:
    value = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    return int(value) if sys.platform == "darwin" else int(value) * 1024


def disk(path: Path) -> dict[str, int]:
    usage = shutil.disk_usage(path)
    return {
        "total": usage.total,
        "used": usage.used,
        "free": usage.free,
    }


def host_info(workdir: Path) -> dict[str, Any]:
    return {
        "hostname": platform.node(),
        "platform": sys.platform,
        "machine": platform.machine(),
        "mac_ver": platform.mac_ver()[0],
        "python": sys.version,
        "python_executable": sys.executable,
        "cpu_count": os.cpu_count(),
        "workdir": str(workdir),
        "disk": disk(workdir),
        "cap_bytes": CAP_BYTES,
        "min_free_disk_bytes": MIN_FREE_DISK_BYTES,
        "bitness": platform.architecture()[0],
    }


@dataclass
class TreeSample:
    tree_rss_bytes: int = 0
    own_rss_bytes: int = 0
    max_single_rss_bytes: int = 0
    processes: int = 0
    samples: int = 0
    exceeded: bool = False
    first_exceeded_at: float | None = None
    last_error: str | None = None


class ProcessTreeMonitor:
    def __init__(
        self, pid: int, *, interval: float = 0.02, cap_bytes: int = CAP_BYTES,
    ) -> None:
        self.pid = pid
        self.interval = interval
        self.cap_bytes = cap_bytes
        self.sample = TreeSample()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._start = time.monotonic()

    def _tree(self) -> list[psutil.Process]:
        root = psutil.Process(self.pid)
        return [root, *root.children(recursive=True)]

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                processes = self._tree()
                values = []
                for process in processes:
                    try:
                        values.append(process.memory_info().rss)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                total = sum(values)
                self.sample.samples += 1
                self.sample.processes = max(self.sample.processes, len(values))
                self.sample.own_rss_bytes = max(
                    self.sample.own_rss_bytes, values[0] if values else 0
                )
                self.sample.max_single_rss_bytes = max(
                    self.sample.max_single_rss_bytes, max(values, default=0)
                )
                self.sample.tree_rss_bytes = max(self.sample.tree_rss_bytes, total)
                if total > self.cap_bytes and not self.sample.exceeded:
                    self.sample.exceeded = True
                    self.sample.first_exceeded_at = time.monotonic() - self._start
            except (psutil.NoSuchProcess, psutil.AccessDenied) as exc:
                self.sample.last_error = type(exc).__name__
            time.sleep(self.interval)

    def __enter__(self) -> "ProcessTreeMonitor":
        self._thread.start()
        return self

    def __exit__(self, *_args: Any) -> None:
        self._stop.set()
        self._thread.join(timeout=2)

    def material(self) -> dict[str, Any]:
        return {
            "tree_peak_rss_bytes": self.sample.tree_rss_bytes,
            "own_peak_rss_bytes": self.sample.own_rss_bytes,
            "max_single_process_peak_rss_bytes": self.sample.max_single_rss_bytes,
            "max_process_count": self.sample.processes,
            "sample_count": self.sample.samples,
            "cap_bytes": self.cap_bytes,
            "cap_exceeded": self.sample.exceeded,
            "first_exceeded_seconds": self.sample.first_exceeded_at,
            "last_sample_error": self.sample.last_error,
            "sampling_interval_seconds": self.interval,
        }


def terminate_tree(pid: int, *, grace_seconds: float = 2.0) -> list[int]:
    terminated: list[int] = []
    try:
        root = psutil.Process(pid)
        processes = [root, *root.children(recursive=True)]
    except psutil.NoSuchProcess:
        return terminated
    for process in reversed(processes):
        try:
            process.send_signal(signal.SIGTERM)
            terminated.append(process.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    deadline = time.monotonic() + grace_seconds
    while time.monotonic() < deadline:
        if all(not p.is_running() for p in processes):
            return terminated
        time.sleep(0.05)
    for process in reversed(processes):
        try:
            process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return terminated


def run_monitored(
    command: list[str], *, cwd: Path, env: dict[str, str],
    timeout_seconds: float, cap_bytes: int = CAP_BYTES,
    interval: float = 0.02,
) -> dict[str, Any]:
    start = time.monotonic()
    process = subprocess.Popen(
        command, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    monitor = ProcessTreeMonitor(process.pid, interval=interval, cap_bytes=cap_bytes)
    monitor.__enter__()
    timed_out = False
    killed_for_cap = False
    try:
        while process.poll() is None:
            if monitor.sample.exceeded:
                killed_for_cap = True
                terminate_tree(process.pid)
                break
            if time.monotonic() - start > timeout_seconds:
                timed_out = True
                terminate_tree(process.pid)
                break
            time.sleep(0.05)
        stdout, stderr = process.communicate(timeout=10)
    finally:
        monitor.__exit__(None, None, None)
    if killed_for_cap or timed_out:
        try:
            stdout, stderr = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
    return {
        "returncode": process.returncode,
        "stdout": stdout,
        "stderr": stderr,
        "seconds": time.monotonic() - start,
        "timed_out": timed_out,
        "killed_for_cap": killed_for_cap,
        "process_tree": monitor.material(),
        "disk_after": disk(cwd),
    }


__all__ = [
    "CAP_BYTES",
    "MIN_FREE_DISK_BYTES",
    "ProcessTreeMonitor",
    "TreeSample",
    "disk",
    "host_info",
    "rss_children_bytes",
    "rss_self_bytes",
    "run_monitored",
    "terminate_tree",
]
