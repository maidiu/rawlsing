"""Test-only transparent writer timing wrapper; no product edit.

Usage later (not run here):
  python3 -B timed_writer.py --snapshot SNAP --out NEW_ROOT \
      --respondents 512 --questions 600 --progress progress.json

The wrapper imports the unchanged writer at 68aa and the existing
build_width512 harness, then wraps only callable boundaries. It writes bounded
progress counters and a final stage breakdown.
"""
from __future__ import annotations

import argparse
import functools
import importlib.util
import json
import os
from pathlib import Path
import sys
import time
from contextlib import contextmanager


ROOT = Path(__file__).resolve().parents[3]
WRITER_SHA = "068fc525b6c117fbb3feba52f740f7e764674ff0b2a78f52e5b649b5fafe643a"
OUT_ROOT = Path(__file__).resolve().parent
PROGRESS_INTERVAL = 8192


class Recorder:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.total = {}
        self.family = {}
        self.stage = {}
        self.events = 0
        self._dirty_at = 0

    def add(self, key: str, seconds: float, count: int = 0) -> None:
        row = self.total.setdefault(key, {"seconds": 0.0, "calls": 0, "count": 0})
        row["seconds"] += seconds
        row["calls"] += 1
        row["count"] += count

    def add_family(self, family: str, key: str, seconds: float, count: int = 0) -> None:
        row = self.family.setdefault(family, {}).setdefault(
            key, {"seconds": 0.0, "calls": 0, "count": 0})
        row["seconds"] += seconds
        row["calls"] += 1
        row["count"] += count

    def mark(self, name: str, detail: str = "") -> None:
        self.stage[name] = {"at": time.time(), "detail": detail}

    def tick(self, count: int = 0) -> None:
        self.events += count
        if self.events - self._dirty_at >= PROGRESS_INTERVAL:
            self.write()
            self._dirty_at = self.events

    def write(self) -> None:
        def sec(key):
            return self.total.get(key, {}).get("seconds", 0.0)
        sink = sum(
            row.get("seconds", 0.0)
            for fam in self.family.values()
            for name, row in fam.items() if name.endswith(".add")
        )
        index = self.total.get("_IndexSink.add", {}).get("seconds", 0.0)
        proof = sec("build_sourcefree_direct_i02")
        writer = sec("write_direct_estate_total")
        verify = sec("_verify_emitted_physical_payloads")
        derived = {
            "sink_add_inclusive": sink,
            "index_add_inclusive": index,
            "proof_residual_not_pure_sql": max(0.0, proof - sink - index),
            "writer_residual_after_proof_verify": max(0.0, writer - proof - verify),
            "note": "nested spans; residual buckets are not pure SQL and may include setup/hash/fsync/publication",
        }
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps({
            "total": self.total,
            "family": self.family,
            "stage": self.stage,
            "derived": derived,
            "events": self.events,
        }, indent=2, sort_keys=True) + "\n")
        os.replace(tmp, self.path)


def _load_build_harness():
    path = Path(
        "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/"
        "MEASUREMENT_PREP/WORKER_RETURNS/"
        "ANVIL_WIDTH512_BOUNDED_CONSTRUCTION_20261118/build_width512.py"
    )
    spec = importlib.util.spec_from_file_location("build_width512_timed", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _wrap(rec: Recorder, owner, name: str, key: str, *, family=False):
    original = getattr(owner, name)

    @functools.wraps(original)
    def wrapped(self, *args, **kwargs):
        start = time.perf_counter()
        try:
            return original(self, *args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start
            if family:
                rec.add_family(self.family, key, elapsed, 1)
            else:
                rec.add(key, elapsed, 1)
            if name == "add":
                rec.tick(1)

    setattr(owner, name, wrapped)


def _verified_writer():
    import rawlsing_next.pre553_source_direct_parquet_estate as writer
    actual = __import__("hashlib").sha256(
        Path(writer.__file__).read_bytes()).hexdigest()
    if actual != WRITER_SHA:
        raise SystemExit(f"WRITER_SHA_MISMATCH:{actual}")
    return writer


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--respondents", type=int, default=512)
    ap.add_argument("--questions", type=int, default=600)
    ap.add_argument("--progress", default=str(OUT_ROOT / "progress.json"))
    args = ap.parse_args()
    progress = Path(args.progress)
    rec = Recorder(progress)
    writer = _verified_writer()
    import rawlsing_next._pre553_direct_i02_sourcefree as proof
    for cls, names in (
        (writer._Sink, ("add", "flush", "close")),
        (writer._IndexSink, ("add", "flush", "close")),
    ):
        for name in names:
            _wrap(rec, cls, name, f"{cls.__name__}.{name}", family=(cls is writer._Sink))
    original_proof = writer.build_sourcefree_direct_i02
    original_verify = writer._verify_emitted_physical_payloads
    original_writer = writer.write_direct_estate

    @functools.wraps(original_proof)
    def proof_timed(*a, **k):
        rec.mark("proof_start")
        with _span(rec, "build_sourcefree_direct_i02"):
            return original_proof(*a, **k)

    @functools.wraps(original_verify)
    def verify_timed(*a, **k):
        rec.mark("verify_start")
        with _span(rec, "_verify_emitted_physical_payloads"):
            return original_verify(*a, **k)

    @functools.wraps(original_writer)
    def writer_timed(*a, **k):
        rec.mark("writer_start")
        with _span(rec, "write_direct_estate_total"):
            return original_writer(*a, **k)

    writer.build_sourcefree_direct_i02 = proof_timed
    writer._verify_emitted_physical_payloads = verify_timed
    writer.write_direct_estate = writer_timed

    # Existing width harness imports write_direct_estate inside main.
    harness = _load_build_harness()
    old_argv = sys.argv
    sys.argv = [
        str(OUT_ROOT / "timed_writer.py"), "--snapshot", args.snapshot,
        "--out", args.out, "--respondents", str(args.respondents),
        "--questions", str(args.questions),
    ]
    try:
        rec.mark("harness_start")
        rc = harness.main()
    finally:
        sys.argv = old_argv
        rec.mark("done", f"rc={rc}")
        rec.write()
    return int(rc)


@contextmanager
def _span(rec: Recorder, key: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        rec.add(key, time.perf_counter() - start)


if __name__ == "__main__":
    raise SystemExit(main())
