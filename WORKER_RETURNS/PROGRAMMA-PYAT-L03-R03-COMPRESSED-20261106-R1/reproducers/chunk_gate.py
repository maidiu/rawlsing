"""R03 independent compressed-body boundary/reconstruction gate."""
from __future__ import annotations

import json
import os
import random
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve()
while not (ROOT / "rawlsing_next").is_dir():
    if ROOT.parent == ROOT:
        raise RuntimeError("repo root not found")
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))
TOOLS = ROOT / "WORKER_RETURNS/PROGRAMMA-PYAT-L03-C4-20261105-R1/tools"
sys.path.insert(0, str(TOOLS))

import bench_common as bc  # noqa: E402
import bench_compact_current as bcc  # noqa: E402
from rawlsing_next import _pre553_c11_execution_view as compact  # noqa: E402
from rawlsing_next.pre553_empirical_objects import canonical_json  # noqa: E402
from rawlsing_next.pre553_source_backed_c11_facade import (  # noqa: E402
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release_from_stream,
)


def main():
    n = 300
    fixture = bcc._source_fixture(n, tag="r03-chunk-gate")
    native = build_validated_source_backed_c11_release_from_stream(
        fixture["stream"], fixture["projection"],
    )
    expected = {
        obj.ref.key: obj for obj in native.public_objects
        if obj.schema_id == "RespondentEvent"
    }
    release = bcc._compact_release(fixture)
    public = release.public_objects
    assert isinstance(public, compact._CompactPublicObjects)
    bodies = public.lane.bodies
    assert isinstance(bodies, compact._CompressedBodies)
    total = len(public.lane.selectors)
    assert total == len(expected) == n * 9
    chunks = list(bodies.chunks)
    counts = [count for _, _, _, count in chunks]
    starts = [start for _, _, start, _ in chunks]
    assert len(chunks) == (total + 255) // 256
    assert all(1 <= count <= 256 for count in counts)
    assert sum(counts) == total
    assert starts == [sum(counts[:i]) for i in range(len(counts))]
    assert bodies.total_rows == total
    last_count = counts[-1]
    assert last_count == total - (len(chunks) - 1) * 256

    order = list(range(total))
    random.Random(0).shuffle(order)
    checked = 0
    for row in order:
        rebuilt = public.lane.materialize(row)
        assert rebuilt.ref == public.lane.selectors[row].ref
        assert rebuilt.as_dict() == expected[public.lane.selectors[row].ref.key].as_dict()
        body = bodies.body_bytes(row)
        assert body == canonical_json(rebuilt.semantic_projection()).encode("utf-8")
        checked += 1
    for row in order[:20] + order[-20:]:
        first = public.lane.materialize(row)
        second = public.lane.materialize(row)
        assert first is not second
        assert first.as_dict() == second.as_dict()
        assert bodies.body_bytes(row) == canonical_json(first.semantic_projection()).encode("utf-8")
    for bad in (-1, total, True):
        try:
            bodies.body_bytes(bad)
        except IndexError:
            pass
        else:
            raise AssertionError(f"expected IndexError for {bad!r}")
    ordered_fields = [
        event for event in expected.values()
        if event.multiplicity_order_rank_fields
    ]
    assert ordered_fields, "fixture has no order/rank/multiplicity fields"
    order_rows = [
        row for row, selector in enumerate(public.lane.selectors)
        if expected[selector.ref.key].multiplicity_order_rank_fields
    ]
    for row in order_rows[:10]:
        assert public.lane.materialize(row).as_dict() == expected[
            public.lane.selectors[row].ref.key
        ].as_dict()

    raw_total = sum(raw_size for _, raw_size, _, _ in chunks)
    compressed_total = sum(len(compressed) for compressed, _, _, _ in chunks)

    # Atomic failure: commit failure must not leave a final or staged file, and
    # the in-memory compact lane must remain exact.
    cache = ROOT / ".local-logs/pyat-l03-r03/chunk-gate-cache"
    if cache.exists():
        shutil.rmtree(cache)
    cache.mkdir(parents=True, mode=0o700)
    old_env = os.environ.get("RAWLSING_C11_ACCELERATOR_DIR")
    os.environ["RAWLSING_C11_ACCELERATOR_DIR"] = str(cache)
    original_commit = compact._BodyCacheWriter.commit

    def failing_commit(self, path):
        raise OSError("R03 injected commit failure")

    compact._BodyCacheWriter.commit = failing_commit
    try:
        failed_public = compact._compact_public_objects(
            native,
            physical_binding=lambda: {"decoder": "r03-chunk-gate"},
            projection_binding="r03-chunk-gate",
        )
    finally:
        compact._BodyCacheWriter.commit = original_commit
        if old_env is None:
            os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
        else:
            os.environ["RAWLSING_C11_ACCELERATOR_DIR"] = old_env
    assert failed_public is not None
    assert isinstance(failed_public.lane.bodies, compact._CompressedBodies)
    assert failed_public.lane.materialize(0).as_dict() == expected[
        failed_public.lane.selectors[0].ref.key
    ].as_dict()
    assert not list(cache.glob("c11-events-*.parquet"))
    assert not list(cache.glob(".c11-events-*"))

    # Atomic replace failure after the writer has closed must also degrade to
    # no-cache, not break the in-memory compact lane or leave staged files.
    original_replace = compact.os.replace

    def failing_replace(src, dst):
        raise OSError("R03 injected atomic replace failure")

    compact.os.replace = failing_replace
    try:
        replace_failed_public = compact._compact_public_objects(
            native,
            physical_binding=lambda: {"decoder": "r03-chunk-gate"},
            projection_binding="r03-chunk-gate",
        )
    finally:
        compact.os.replace = original_replace
    assert replace_failed_public is not None
    assert isinstance(replace_failed_public.lane.bodies, compact._CompressedBodies)
    assert replace_failed_public.lane.materialize(0).as_dict() == expected[
        replace_failed_public.lane.selectors[0].ref.key
    ].as_dict()
    assert not list(cache.glob("c11-events-*.parquet"))
    assert not list(cache.glob(".c11-events-*"))

    # Old-reader-compatible cache format: rewrite the raw-body Parquet as one
    # legacy-style row group and reread it through the new reader.
    if cache.exists():
        shutil.rmtree(cache)
    cache.mkdir(parents=True, mode=0o700)
    os.environ["RAWLSING_C11_ACCELERATOR_DIR"] = str(cache)
    try:
        _repo, cached_release = build_source_backed_c11_repository(
            fixture["stream"], fixture["projection"],
            current_authorities=fixture["projection"].authority_snapshots,
        )
    finally:
        if old_env is None:
            os.environ.pop("RAWLSING_C11_ACCELERATOR_DIR", None)
        else:
            os.environ["RAWLSING_C11_ACCELERATOR_DIR"] = old_env
    path, = cache.glob("c11-events-*.parquet")
    import pyarrow as pa
    import pyarrow.parquet as pq

    schema = pq.read_schema(path)
    key = schema.metadata[compact._CACHE_METADATA_KEY].decode("ascii")
    old_rows = pq.read_table(path).to_pylist()
    old_style = pa.table({
        compact._EVENT_BODY_COLUMN: pa.array(
            [row[compact._EVENT_BODY_COLUMN] for row in old_rows], type=pa.binary(),
        ),
    }).replace_schema_metadata(schema.metadata)
    pq.write_table(old_style, path, compression="zstd", compression_level=3)
    reread = compact._read_bodies(path, key, cached_release.public_objects.lane.selectors)
    assert isinstance(reread, compact._CompressedBodies)
    for row in order[:128] + order[-32:]:
        assert reread.body_bytes(row) == bodies.body_bytes(row)
    assert reread.body_bytes(0) == canonical_json(
        expected[cached_release.public_objects.lane.selectors[0].ref.key].semantic_projection()
    ).encode("utf-8")

    # Lookup microbenchmark: one chunk decompression or one materialize per row,
    # 256 rows per pass; report medians only.
    rows = list(range(256))
    passes = []
    for _ in range(3):
        start = time.perf_counter()
        for row in rows:
            bodies.body_bytes(row)
        decompress_wall = time.perf_counter() - start
        start = time.perf_counter()
        for row in rows:
            public.lane.materialize(row)
        materialize_wall = time.perf_counter() - start
        passes.append((decompress_wall, materialize_wall))
    passes.sort()
    decompress_median, materialize_median = passes[1]
    payload = {
        "schema": "R03_COMPRESSED_BODY_GATE@1",
        "implementation_sha": "02c1200b82b8397e551817e8e4cf2c6763413189",
        "n": n,
        "event_count": total,
        "chunk_event_limit": compact._EVENT_BODY_CHUNK_EVENTS,
        "chunk_count": len(chunks),
        "chunk_counts": counts,
        "last_chunk_count": last_count,
        "chunk_starts_contiguous": True,
        "raw_bytes": raw_total,
        "compressed_bytes": compressed_total,
        "compression_ratio": (raw_total / compressed_total) if compressed_total else None,
        "random_repeated_lookup_rows_checked": checked,
        "order_rank_rows_checked": len(order_rows[:10]),
        "detached_selector_refs_equal": True,
        "out_of_range_index_error": True,
        "atomic_commit_failure_cleanup": True,
        "atomic_replace_failure_cleanup": True,
        "old_reader_style_readback": True,
        "lookup_ms_per_event": {
            "decompress_median": decompress_median / 256 * 1000,
            "materialize_median": materialize_median / 256 * 1000,
            "passes": [
                [d / 256 * 1000, m / 256 * 1000] for d, m in passes
            ],
        },
        "all_pass": True,
    }
    out = ROOT / ".local-logs/pyat-l03-r03/chunk_gate.json"
    out.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(json.dumps({k: payload[k] for k in (
        "all_pass", "event_count", "chunk_count", "chunk_counts", "last_chunk_count",
        "raw_bytes", "compressed_bytes", "compression_ratio",
        "lookup_ms_per_event",
    )}, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
