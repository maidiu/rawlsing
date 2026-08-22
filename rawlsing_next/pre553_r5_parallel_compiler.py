"""Execution-only Compact V2 parallel-12 compiler.

The decoder remains coordinator-owned. Workers only encode already normalized
canonical rows into bounded sorted run files; the frozen Compact V2 builder
still owns final shard, inventory, root, and audit law.
"""
from __future__ import annotations

from concurrent.futures import Future, ProcessPoolExecutor, wait, FIRST_COMPLETED
from dataclasses import dataclass
import hashlib
import heapq
import json
import os
from pathlib import Path
import resource
import shutil
import tempfile
import time
from typing import Any, Iterable, Iterator, Mapping, Sequence
import multiprocessing as mp

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_r5_compact_carrier import R5LongShardedBuilder, _logical_wire, ROW_SCHEMA_VERSION
from rawlsing_next.pre553_r5_compact_density_court import WVS_EVENTS, _source_rows
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5CanonicalRow


WORKER_COUNT = 12
QUEUE_CAPACITY = 12
RSS_SOFT_BYTES = int(2.5 * 1024**3)
RSS_DRAIN_BYTES = int(3.0 * 1024**3)
RSS_HARD_BYTES = int(3.5 * 1024**3)
SCRATCH_WARN_BYTES = 6 * 1024**3
SCRATCH_HARD_BYTES = 8 * 1024**3
FREE_HARD_BYTES = 5 * 1024**3


@dataclass(frozen=True)
class ParallelConfig:
    workers: int = WORKER_COUNT
    queue_capacity: int = QUEUE_CAPACITY
    batch_rows: int = 4096

    def __post_init__(self) -> None:
        if self.workers != WORKER_COUNT:
            raise ValueError("parallel-12 court requires exactly 12 compiler workers")
        if self.queue_capacity < 1 or self.queue_capacity > QUEUE_CAPACITY:
            raise ValueError("queue capacity must be between 1 and 12")
        if self.batch_rows < 1:
            raise ValueError("batch_rows must be positive")


def _worker_sort(rows: Sequence[R5CanonicalRow]) -> tuple[bytes, ...]:
    """Worker-only physical encoding and deterministic local sort."""
    return tuple(sorted(_logical_wire(row) for row in rows))


def _decode_logical(line: bytes) -> R5CanonicalRow:
    item = json.loads(line.decode("ascii"))
    if item.get("row_schema_version") != ROW_SCHEMA_VERSION:
        raise RuntimeError("parallel logical run schema mismatch")
    return R5CanonicalRow(item["relation"], item["object_family"], item["object_id"], item["content_hash"], item["payload"])


def _rss_tree_bytes() -> tuple[int, int, int]:
    try:
        import psutil
        parent = psutil.Process(os.getpid())
        processes = [parent, *parent.children(recursive=True)]
        values = [int(p.memory_info().rss) for p in processes if p.is_running()]
        return sum(values), int(parent.memory_info().rss), max(values or [0])
    except Exception:
        value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        if os.uname().sysname != "Darwin": value *= 1024
        return value, value, value


def _dir_bytes(path: Path) -> int:
    total = 0
    if path.exists():
        for base, _dirs, files in os.walk(path):
            for name in files:
                try: total += (Path(base) / name).stat().st_size
                except FileNotFoundError: pass
    return total


def _free_bytes(path: Path) -> int:
    return int(os.statvfs(path).f_bavail * os.statvfs(path).f_frsize)


def _merge_runs(run_paths: Sequence[Path]) -> Iterator[R5CanonicalRow]:
    handles = [path.open("rb") for path in run_paths]
    try:
        heap: list[tuple[bytes, int]] = []
        for index, handle in enumerate(handles):
            line = handle.readline()
            if line: heapq.heappush(heap, (line, index))
        previous: bytes | None = None
        while heap:
            line, index = heapq.heappop(heap)
            if previous is not None and line <= previous:
                raise RuntimeError("parallel run merge found duplicate/noncanonical row")
            previous = line
            yield _decode_logical(line)
            nxt = handles[index].readline()
            if nxt: heapq.heappush(heap, (nxt, index))
    finally:
        for handle in handles: handle.close()


def build_parallel(source: Path, checkpoint: int, work_root: Path, *,
                   config: ParallelConfig | None = None) -> Mapping[str, Any]:
    config = config or ParallelConfig()
    if checkpoint < 1 or checkpoint > WVS_EVENTS: raise ValueError("invalid checkpoint")
    work_root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f"p12-{checkpoint}-", dir=work_root))
    runs_dir = staging / "worker-runs"; runs_dir.mkdir()
    target = staging / "sealed"
    started = time.perf_counter(); last = started; last_cells = 0; peak_rss = 0; max_queue = 0
    worker_failures = 0; batch_index = 0; cells = 0; source_rows = 0; futures: set[Future] = set(); run_paths: list[Path] = []

    def heartbeat(phase: str, force: bool = False) -> None:
        nonlocal last, last_cells, peak_rss, max_queue
        now = time.perf_counter(); aggregate, coordinator, _ = _rss_tree_bytes(); peak_rss = max(peak_rss, aggregate)
        scratch = _dir_bytes(staging); free = _free_bytes(staging)
        max_queue = max(max_queue, len(futures))
        if not force and cells - last_cells < 500_000 and now - last < 60: return
        rate = (cells-last_cells)/(now-last) if now > last and cells > last_cells else 0.0
        eta = (WVS_EVENTS-cells)/rate if rate else None
        print(f"[R5/P12][{phase}] {cells:,}/{checkpoint:,} cells | workers {config.workers}/12 | "
              f"queue {len(futures)}/{config.queue_capacity} | RSS {aggregate} peak {peak_rss} | "
              f"coord {coordinator} | scratch {scratch} | {rate:.0f} cells/s | elapsed {now-started:.1f}s | ETA {eta}", flush=True)
        last = now; last_cells = cells
        if aggregate >= RSS_HARD_BYTES: raise RuntimeError("R5_PARALLEL12_BLOCKED__AGGREGATE_RSS_HARD_GATE")
        if scratch >= SCRATCH_HARD_BYTES: raise RuntimeError("R5_PARALLEL12_BLOCKED__SCRATCH_HARD_GATE")
        if free < FREE_HARD_BYTES: raise RuntimeError("R5_PARALLEL12_BLOCKED__FREE_SPACE_HARD_GATE")

    def harvest(done: set[Future]) -> None:
        nonlocal worker_failures
        for future in done:
            try: encoded = future.result()
            except Exception as exc:
                worker_failures += 1
                raise RuntimeError("R5_PARALLEL12_BLOCKED__PROCESS_PROTOCOL") from exc
            path = runs_dir / f"run-{len(run_paths):08d}.r5r"
            with path.open("wb") as handle:
                for line in encoded: handle.write(line)
            run_paths.append(path)

    heartbeat("START", force=True)
    try:
        incidence = decode_sav(source)
        if incidence.source_sha256 != "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d":
            raise RuntimeError("R5_PARALLEL12_BLOCKED__SOURCE_IDENTITY")
        if incidence.row_count != 97220 or len(incidence.variables) != 613:
            raise RuntimeError("R5_PARALLEL12_BLOCKED__SOURCE_SHAPE")
        heartbeat("SOURCE_VERIFY", force=True)
        ctx = mp.get_context("spawn")
        with ProcessPoolExecutor(max_workers=WORKER_COUNT, mp_context=ctx) as executor:
            batch: list[R5CanonicalRow] = []
            for row in _source_rows(incidence, checkpoint, 250_000):
                batch.append(row)
                if row.relation == "source_physical_cells":
                    cells += 1; source_rows = max(source_rows, int(row.payload["row_ordinal"]))
                if len(batch) >= config.batch_rows:
                    while len(futures) >= config.queue_capacity:
                        done, pending = wait(futures, return_when=FIRST_COMPLETED); futures = set(pending); harvest(done); heartbeat("COMPILE")
                    futures.add(executor.submit(_worker_sort, tuple(batch))); batch = []; batch_index += 1; heartbeat("DISPATCH")
            if batch:
                futures.add(executor.submit(_worker_sort, tuple(batch)))
                batch_index += 1
            while futures:
                done, pending = wait(futures, return_when=FIRST_COMPLETED); futures = set(pending); harvest(done); heartbeat("MERGE_RUNS", force=not futures)
        if len(run_paths) != batch_index:
            raise RuntimeError("R5_PARALLEL12_BLOCKED__PROCESS_PROTOCOL")
        heartbeat("FINAL_SERIAL_COMPACT_SEAL", force=True)
        serial_builder = R5LongShardedBuilder()
        telemetry = serial_builder.build(_merge_runs(run_paths), release_identity=__import__("rawlsing_next.pre553_r5_compact_density_court", fromlist=["_release_identity"])._release_identity(checkpoint), target_directory=target)
        elapsed = time.perf_counter() - started
        aggregate, coordinator, worker_peak = _rss_tree_bytes(); peak_rss = max(peak_rss, aggregate)
        result = {**telemetry, "checkpoint": checkpoint, "workers": WORKER_COUNT, "queue_capacity": config.queue_capacity,
                  "max_queue_occupancy": max_queue, "source_rows_reached": source_rows, "physical_cells": cells,
                  "parallel_build_seconds": elapsed, "aggregate_peak_rss_bytes": peak_rss, "coordinator_rss_bytes": coordinator,
                  "worker_peak_rss_bytes": worker_peak, "scratch_peak_bytes": _dir_bytes(staging), "worker_failures": worker_failures,
                  "persistent_cache_count": 0, "source_sha256": incidence.source_sha256, "target": str(target)}
        print(json.dumps(result, sort_keys=True), flush=True)
        return result
    except Exception:
        worker_failures += 1
        raise


def cleanup(result: Mapping[str, Any]) -> None:
    target = Path(str(result["target"])); shutil.rmtree(target.parent, ignore_errors=True)


__all__ = ["WORKER_COUNT", "QUEUE_CAPACITY", "ParallelConfig", "build_parallel", "cleanup"]
