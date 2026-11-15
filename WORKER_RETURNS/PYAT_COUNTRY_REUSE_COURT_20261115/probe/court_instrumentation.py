"""Test-only runtime instrumentation and resource snapshots for the reuse court.

Nothing here edits production source.  Wrappers count calls at existing public
or private runtime boundaries and always invoke the accepted implementation.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import time
from typing import Any, Iterator


def directory_bytes(path: str | Path) -> int:
    try:
        return sum(
            item.stat().st_size for item in Path(path).rglob("*") if item.is_file()
        )
    except FileNotFoundError:
        return 0


def maxrss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if sys.platform == "darwin" else value * 1024


def cpu_times() -> dict[str, float]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "user_seconds": float(usage.ru_utime),
        "system_seconds": float(usage.ru_stime),
        "maxrss_bytes": maxrss_bytes(),
    }


def current_rss_bytes() -> int:
    try:
        text = subprocess.check_output(
            ["ps", "-o", "rss=", "-p", str(os.getpid())], text=True
        ).strip()
        return int(text) * 1024
    except (OSError, ValueError, subprocess.SubprocessError):
        return maxrss_bytes()


def process_tree_rss_bytes(pid: int | None = None) -> int:
    """Sum RSS for a process and all of its descendants (single process here)."""
    pid = os.getpid() if pid is None else pid
    try:
        text = subprocess.check_output(
            ["ps", "-axo", "pid=,ppid=,rss="], text=True
        )
    except (OSError, subprocess.SubprocessError):
        return current_rss_bytes()
    rows: list[tuple[int, int, int]] = []
    for line in text.splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        try:
            rows.append((int(parts[0]), int(parts[1]), int(parts[2])))
        except ValueError:
            continue
    children: dict[int, list[tuple[int, int]]] = {}
    rss_by_pid: dict[int, int] = {}
    for item_pid, parent_pid, rss_kb in rows:
        children.setdefault(parent_pid, []).append((item_pid, rss_kb))
        rss_by_pid[item_pid] = rss_kb
    total = 0
    stack = [pid]
    seen = set()
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        total += rss_by_pid.get(current, 0)
        stack.extend(child for child, _ in children.get(current, ()))
    return total * 1024


def _run_text(command: list[str], *, timeout: int = 20) -> str:
    try:
        return subprocess.check_output(command, text=True, stderr=subprocess.STDOUT, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"UNKNOWN: {exc}"


def preflight_snapshot(*, repo: Path) -> dict[str, Any]:
    import importlib.metadata as metadata

    def version(name: str) -> str | None:
        try:
            return metadata.version(name)
        except metadata.PackageNotFoundError:
            return None

    ps = _run_text(["ps", "-Ao", "pid,ppid,pcpu,pmem,rss,comm"])
    rawlsing = [
        line for line in ps.splitlines()
        if "Rawlsing" in line and str(os.getpid()) not in line.split()[:1]
    ]
    load = os.getloadavg() if hasattr(os, "getloadavg") else (None, None, None)
    return {
        "schema": "PYAT_COUNTRY_REUSE_PREFLIGHT@1",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "pid": os.getpid(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python": sys.version,
        "cpu_count": os.cpu_count(),
        "load_average_1_5_15": list(load),
        "packages": {
            name: version(name)
            for name in ("pyarrow", "duckdb", "pyreadstat", "pandas", "numpy")
        },
        "git_head": _run_text(["git", "rev-parse", "HEAD"], timeout=10).strip() if (repo / ".git").exists() or True else None,
        "git_branch": _run_text(["git", "rev-parse", "--abbrev-ref", "HEAD"], timeout=10).strip(),
        "git_status_short": _run_text(["git", "status", "--short", "--branch"], timeout=10),
        "estate_disk": shutil.disk_usage(str(repo)),
        "other_rawlsing_process_lines": rawlsing[:20],
        "other_rawlsing_process_count": len(rawlsing),
        "top_cpu_lines": "\n".join(ps.splitlines()[:12]),
        "uptime": _run_text(["uptime"]),
        "vm_stat": _run_text(["vm_stat"]),
        "df": _run_text(["df", "-h", str(repo)]),
    }


@dataclass
class CourtCounters:
    row_group_reads: int = 0
    row_group_rows: int = 0
    row_group_compressed_bytes: int = 0
    row_group_uncompressed_bytes: int = 0
    read_table_calls: int = 0
    session_opens: int = 0
    session_builds: int = 0
    session_enter_seconds: float = 0.0
    session_build_seconds: float = 0.0
    session_temp_max_bytes: int = 0
    selected_event_calls: int = 0
    selected_events_yielded: int = 0
    family_calls: int = 0
    family_rows_yielded: int = 0
    family_object_materializations: int = 0
    event_object_materializations: int = 0
    c11_repository_tripwire_hits: int = 0
    read_table_tripwire_hits: int = 0
    _originals: dict[str, Any] = field(default_factory=dict)

    def material(self) -> dict[str, Any]:
        return {
            "row_group_reads": self.row_group_reads,
            "row_group_rows": self.row_group_rows,
            "row_group_compressed_bytes": self.row_group_compressed_bytes,
            "row_group_uncompressed_bytes": self.row_group_uncompressed_bytes,
            "read_table_calls": self.read_table_calls,
            "session_opens": self.session_opens,
            "session_builds": self.session_builds,
            "session_enter_seconds": self.session_enter_seconds,
            "session_build_seconds": self.session_build_seconds,
            "session_temp_max_bytes": self.session_temp_max_bytes,
            "selected_event_calls": self.selected_event_calls,
            "selected_events_yielded": self.selected_events_yielded,
            "family_calls": self.family_calls,
            "family_rows_yielded": self.family_rows_yielded,
            "family_object_materializations": self.family_object_materializations,
            "event_object_materializations": self.event_object_materializations,
            "c11_repository_tripwire_hits": self.c11_repository_tripwire_hits,
            "read_table_tripwire_hits": self.read_table_tripwire_hits,
        }


class CourtInstrumentation:
    """Install/restore exact-count wrappers for one measured phase."""

    def __init__(self) -> None:
        self.counters = CourtCounters()
        self._active = False

    def install(self, *, forbid_c11_repository: bool = True) -> None:
        if self._active:
            raise RuntimeError("instrumentation already active")
        import pyarrow.parquet as pq
        from rawlsing_next import pre553_direct_estate_i03 as direct
        from rawlsing_next import pre553_source_direct_parquet_estate as estate
        from rawlsing_next.pre553_c11_repository import C11Repository

        c = self.counters

        original_read_row_group = pq.ParquetFile.read_row_group

        def read_row_group(self, *args, **kwargs):
            result = original_read_row_group(self, *args, **kwargs)
            gid = kwargs.get("i")
            if gid is None and args:
                gid = args[0]
            try:
                gid = int(gid)
                group = self.metadata.row_group(gid)
                compressed = sum(
                    int(group.column(index).total_compressed_size)
                    for index in range(group.num_columns)
                )
                c.row_group_reads += 1
                c.row_group_rows += int(group.num_rows)
                c.row_group_compressed_bytes += compressed
                c.row_group_uncompressed_bytes += int(group.total_byte_size)
            except Exception:
                c.row_group_reads += 1
            return result

        original_read_table = pq.read_table

        def read_table(*args, **kwargs):
            c.read_table_calls += 1
            if forbid_c11_repository:
                c.read_table_tripwire_hits += 1
                raise RuntimeError("whole-table read is forbidden in the cold saved court")
            return original_read_table(*args, **kwargs)

        original_family_object = direct._object_from_row
        original_event_object = estate._object_from_row

        def family_object(value):
            c.family_object_materializations += 1
            return original_family_object(value)

        def event_object(value):
            c.event_object_materializations += 1
            return original_event_object(value)

        original_enter = direct.DirectEstateI03Session.__enter__
        original_build = direct.DirectEstateI03Session._build
        original_exit = direct.DirectEstateI03Session.__exit__
        original_selected = direct.DirectEstateI03Session._selected_events
        original_family = direct.DirectEstateI03Session._respondent_family
        original_c11_init = C11Repository.__init__

        def enter(self):
            c.session_opens += 1
            start = time.monotonic()
            try:
                return original_enter(self)
            finally:
                c.session_enter_seconds += time.monotonic() - start

        def build(self):
            c.session_builds += 1
            start = time.monotonic()
            try:
                return original_build(self)
            finally:
                c.session_build_seconds += time.monotonic() - start

        def exit_(self, exc_type, exc, tb):
            temporary = getattr(self, "_temporary", None)
            if temporary is not None:
                c.session_temp_max_bytes = max(
                    c.session_temp_max_bytes, directory_bytes(temporary.name)
                )
            return original_exit(self, exc_type, exc, tb)

        def selected(self, *args, **kwargs):
            c.selected_event_calls += 1
            for event in original_selected(self, *args, **kwargs):
                c.selected_events_yielded += 1
                yield event

        def family(self, *args, **kwargs):
            c.family_calls += 1
            for row in original_family(self, *args, **kwargs):
                c.family_rows_yielded += 1
                yield row

        def c11_init(self, *args, **kwargs):
            c.c11_repository_tripwire_hits += 1
            if forbid_c11_repository:
                raise RuntimeError("full C11Repository build is forbidden in the cold saved court")
            return original_c11_init(self, *args, **kwargs)

        self._originals = {
            "pq_read_row_group": original_read_row_group,
            "pq_read_table": original_read_table,
            "family_object": original_family_object,
            "event_object": original_event_object,
            "enter": original_enter,
            "build": original_build,
            "exit": original_exit,
            "selected": original_selected,
            "family": original_family,
            "c11_init": original_c11_init,
            "pq": pq,
            "direct": direct,
            "estate": estate,
            "C11Repository": C11Repository,
        }
        pq.ParquetFile.read_row_group = read_row_group
        pq.read_table = read_table
        direct._object_from_row = family_object
        estate._object_from_row = event_object
        direct.DirectEstateI03Session.__enter__ = enter
        direct.DirectEstateI03Session._build = build
        direct.DirectEstateI03Session.__exit__ = exit_
        direct.DirectEstateI03Session._selected_events = selected
        direct.DirectEstateI03Session._respondent_family = family
        C11Repository.__init__ = c11_init
        self._active = True

    def restore(self) -> None:
        if not self._active:
            return
        o = self._originals
        o["pq"].ParquetFile.read_row_group = o["pq_read_row_group"]
        o["pq"].read_table = o["pq_read_table"]
        o["direct"]._object_from_row = o["family_object"]
        o["estate"]._object_from_row = o["event_object"]
        o["direct"].DirectEstateI03Session.__enter__ = o["enter"]
        o["direct"].DirectEstateI03Session._build = o["build"]
        o["direct"].DirectEstateI03Session.__exit__ = o["exit"]
        o["direct"].DirectEstateI03Session._selected_events = o["selected"]
        o["direct"].DirectEstateI03Session._respondent_family = o["family"]
        o["C11Repository"].__init__ = o["c11_init"]
        self._active = False

    @contextmanager
    def phase(self, *, forbid_c11_repository: bool = True) -> Iterator[CourtCounters]:
        self.install(forbid_c11_repository=forbid_c11_repository)
        try:
            yield self.counters
        finally:
            self.restore()


__all__ = [
    "CourtCounters",
    "CourtInstrumentation",
    "cpu_times",
    "current_rss_bytes",
    "directory_bytes",
    "maxrss_bytes",
    "preflight_snapshot",
    "process_tree_rss_bytes",
]
