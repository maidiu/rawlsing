"""Independent process-tree/disk monitor for the R2 recheck."""
from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import threading
import time
from typing import Any

import psutil

CAP_BYTES = 6 * 1024 ** 3
MIN_FREE_DISK_BYTES = 3 * 1024 ** 3


def disk(path: Path) -> dict[str, int]:
    usage = shutil.disk_usage(path)
    return {"total": usage.total, "used": usage.used, "free": usage.free}


def directory_bytes(path: Path) -> int:
    try:
        return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())
    except FileNotFoundError:
        return 0


class TreeMonitor:
    def __init__(self, pid: int, *, watch: Path, interval: float = 0.05) -> None:
        self.pid = pid
        self.watch = watch
        self.interval = interval
        self.peak_tree = 0
        self.peak_single = 0
        self.max_processes = 0
        self.samples = 0
        self.peak_watch = 0
        self.min_free = disk(watch)["free"]
        self.exceeded = False
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
                self.peak_single = max(self.peak_single, max(values, default=0))
                self.peak_tree = max(self.peak_tree, total)
                if total > CAP_BYTES:
                    self.exceeded = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
            try:
                self.peak_watch = max(self.peak_watch, directory_bytes(self.watch))
                self.min_free = min(self.min_free, disk(self.watch)["free"])
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
            "tree_peak_rss_bytes": self.peak_tree,
            "max_single_process_peak_rss_bytes": self.peak_single,
            "max_process_count": self.max_processes,
            "sample_count": self.samples,
            "peak_watch_bytes": self.peak_watch,
            "min_free_disk_bytes": self.min_free,
            "cap_bytes": CAP_BYTES,
            "cap_exceeded": self.exceeded,
            "sampling_interval_seconds": self.interval,
        }


def terminate_tree(pid: int, grace: float = 2.0) -> None:
    try:
        root = psutil.Process(pid)
        processes = [root, *root.children(recursive=True)]
    except psutil.NoSuchProcess:
        return
    for process in reversed(processes):
        try:
            process.send_signal(signal.SIGTERM)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    deadline = time.monotonic() + grace
    while time.monotonic() < deadline:
        if all(not p.is_running() for p in processes):
            return
        time.sleep(0.05)
    for process in reversed(processes):
        try:
            process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def run_monitored(
    command: list[str], *, cwd: Path, env: dict[str, str],
    timeout_seconds: float, watch: Path,
) -> dict[str, Any]:
    start = time.monotonic()
    process = subprocess.Popen(
        command, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    monitor = TreeMonitor(process.pid, watch=watch)
    monitor.__enter__()
    timed_out = False
    killed_for_cap = False
    try:
        while process.poll() is None:
            if monitor.exceeded:
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
        "disk_after": disk(watch),
    }
