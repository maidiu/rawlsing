"""Execution-only exact WVS prefix density court for compact R5 LONG V2.

Authority 63 requires actual sealed member+inventory+root bytes at representative
real-source prefixes before another full-source run. This runner makes no source
semantic claims and never modifies frozen decoder/C11/I03/I05/I04 law.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import threading
import time
from typing import Iterable

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec, canonical_json
from rawlsing_next.pre553_r5_compact_carrier import (
    R5LongShardedBuilder,
    R5LongShardedReader,
)
from rawlsing_next.pre553_r5_model import R5BuildConfig, R5CanonicalRow, R5ReleaseIdentity
from rawlsing_next.pre553_r5_seam import (
    cell_record_row,
    normalize_decoder_batch,
    normalize_variables,
    source_metadata_row,
    variable_record_row,
)

WVS_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
WVS_ROWS = 97_220
WVS_VARIABLES = 613
WVS_EVENTS = 59_595_860
PREFERRED_BYTES_PER_EVENT = 36.0
HARD_BYTES_PER_EVENT = 72.0


def _h(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _release_identity(checkpoint: int) -> R5ReleaseIdentity:
    label = f"R5_COMPACT_DENSITY_EXECUTION_ONLY:{WVS_SHA256}:{checkpoint}"
    return R5ReleaseIdentity(
        release_id=f"R5-COMPACT-WVS-PREFIX-{checkpoint}",
        semantic_release_hash=_h(label + ":semantic"),
        source_artifact_ref={
            "kind": "SOURCE_ARTIFACT",
            "object_id": f"sha256:{WVS_SHA256}",
            "content_hash": WVS_SHA256,
        },
        source_release_manifest_hash=_h(label + ":manifest"),
        m01_m18_coverage={
            f"M{i:02d}": ("DENSITY_EXECUTION_ONLY__NO_SEMANTIC_CERTIFICATION",)
            for i in range(1, 19)
        },
        decoder_receipt={
            "decoder": "decode_sav",
            "encoding_override": None,
            "authority_status": "DENSITY_EXECUTION_ONLY__FROZEN_DECODER",
        },
        compiler_contract_digest=_h("R5_LONG_COMPACT_V2_DENSITY_COURT"),
        c11_authority_digest=_h("FROZEN_C11_UNCHANGED"),
    )


def _peak_rss_bytes() -> int:
    value = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return value if os.uname().sysname == "Darwin" else value * 1024


def _directory_bytes(root: Path) -> int:
    total = 0
    if not root.exists():
        return 0
    for base, _dirs, files in os.walk(root):
        for name in files:
            try:
                total += (Path(base) / name).stat().st_size
            except FileNotFoundError:
                pass
    return total


class _ScratchMonitor:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.peak_bytes = 0
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)

    def _run(self) -> None:
        while not self._stop.wait(1.0):
            self.peak_bytes = max(self.peak_bytes, _directory_bytes(self.root))

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.peak_bytes = max(self.peak_bytes, _directory_bytes(self.root))
        self._stop.set()
        self._thread.join(timeout=5)


def _source_rows(incidence, checkpoint: int, progress_every: int) -> Iterable[R5CanonicalRow]:
    codec = R5TypedValueCodec()
    yield source_metadata_row(incidence, codec=codec)
    for variable in normalize_variables(incidence, codec=codec):
        yield variable_record_row(variable)

    emitted = 0
    started = time.perf_counter()
    next_progress = progress_every
    for physical_batch in incidence.iter_batches(batch_size=8192):
        normalized = normalize_decoder_batch(
            incidence.source_sha256,
            physical_batch,
            codec=codec,
            geometry=None,
            permit_vector_hot_path=True,
            validate_vector_parity=True,
        )
        for cell in normalized.cells:
            if emitted >= checkpoint:
                return
            yield cell_record_row(cell)
            emitted += 1
            if emitted >= next_progress or emitted == checkpoint:
                elapsed = time.perf_counter() - started
                rate = emitted / elapsed if elapsed else 0.0
                print(
                    f"[R5-COMPACT/WVS][PREFIX_BUILD] {emitted:,}/{checkpoint:,} "
                    f"cells ({100.0 * emitted / checkpoint:.2f}%) | "
                    f"peak RSS {_peak_rss_bytes() / (1024**2):.1f} MiB | "
                    f"elapsed {elapsed:.1f}s | {rate:,.0f} cells/s",
                    flush=True,
                )
                next_progress += progress_every
    if emitted != checkpoint:
        raise RuntimeError(f"WVS prefix frontier ended early: {emitted} != {checkpoint}")


def run(source: Path, checkpoint: int, work_root: Path, *, keep: bool = False) -> dict:
    if checkpoint not in {250_000, 1_000_000, 2_000_000}:
        raise ValueError("checkpoint must be one of 250000, 1000000, 2000000")
    work_root.mkdir(parents=True, exist_ok=True)
    target = work_root / f"sealed-{checkpoint}"
    if target.exists():
        shutil.rmtree(target)

    opened = time.perf_counter()
    incidence = decode_sav(source)
    if incidence.source_sha256 != WVS_SHA256:
        raise RuntimeError("R5_LONG_COMPACT_V2_BLOCKED__SOURCE_IDENTITY")
    if incidence.row_count != WVS_ROWS or len(incidence.variables) != WVS_VARIABLES:
        raise RuntimeError("R5_LONG_COMPACT_V2_BLOCKED__SOURCE_SHAPE")
    decoder_open_seconds = time.perf_counter() - opened

    config = R5BuildConfig(
        run_max_rows=4096,
        run_max_bytes=4 * 1024 * 1024,
        shard_max_rows=16384,
        shard_max_bytes=16 * 1024 * 1024,
        merge_fan_in=8,
        verified_spool_memory_bytes=1024 * 1024,
    )
    started = time.perf_counter()
    with _ScratchMonitor(target) as monitor:
        telemetry = R5LongShardedBuilder(config).build(
            _source_rows(incidence, checkpoint, 250_000),
            release_identity=_release_identity(checkpoint),
            target_directory=target,
        )
    build_seconds = time.perf_counter() - started

    reopen_started = time.perf_counter()
    reader = R5LongShardedReader(
        target, expected_physical_root_id=telemetry["physical_root_id"]
    )
    audit = reader.full_audit()
    reopen_audit_seconds = time.perf_counter() - reopen_started

    expected_rows = checkpoint + WVS_VARIABLES + 1
    if audit["canonical_rows"] != expected_rows:
        raise RuntimeError(
            f"compact prefix audit frontier mismatch {audit['canonical_rows']} != {expected_rows}"
        )

    steady = int(telemetry["canonical_steady_state_bytes"])
    density = steady / checkpoint
    projected = density * WVS_EVENTS
    if density <= PREFERRED_BYTES_PER_EVENT:
        disposition = "R5_LONG_COMPACT_V2_DENSITY_PASS__PREFERRED"
    elif density <= HARD_BYTES_PER_EVENT:
        disposition = "R5_LONG_COMPACT_V2_DENSITY_RETURNED__HQ_ADJUDICATION_REQUIRED"
    else:
        disposition = "R5_LONG_COMPACT_V2_BLOCKED__DENSITY_HARD_GATE"

    result = {
        "source_sha256": incidence.source_sha256,
        "source_rows": incidence.row_count,
        "source_variables": len(incidence.variables),
        "physical_cells_checkpoint": checkpoint,
        "canonical_rows_including_source_and_variable_metadata": expected_rows,
        "member_bytes": telemetry["member_bytes"],
        "inventory_bytes": telemetry["inventory_bytes"],
        "root_bytes": telemetry["root_bytes"],
        "canonical_steady_state_bytes": steady,
        "actual_sealed_bytes_per_physical_cell": density,
        "projected_full_wvs_bytes": projected,
        "projected_full_wvs_gib": projected / (1024**3),
        "preferred_bytes_per_event": PREFERRED_BYTES_PER_EVENT,
        "hard_bytes_per_event": HARD_BYTES_PER_EVENT,
        "decoder_open_seconds": decoder_open_seconds,
        "build_seconds": build_seconds,
        "reopen_full_audit_seconds": reopen_audit_seconds,
        "peak_rss_bytes": _peak_rss_bytes(),
        "scratch_peak_bytes_observed": monitor.peak_bytes,
        "final_shards": telemetry["final_shards"],
        "initial_runs": telemetry["initial_runs"],
        "merge_passes": telemetry["merge_passes"],
        "logical_stream_digest": telemetry["logical_stream_digest"],
        "audit_logical_stream_digest": audit["logical_stream_digest"],
        "persistent_cache_count": 0,
        "worker_count": 1,
        "disposition": disposition,
    }
    if result["logical_stream_digest"] != result["audit_logical_stream_digest"]:
        raise RuntimeError("R5_LONG_COMPACT_V2_BLOCKED__LOGICAL_AUDIT_MISMATCH")

    print(canonical_json(result), flush=True)
    if not keep:
        shutil.rmtree(target)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--checkpoint", type=int, required=True)
    parser.add_argument("--work-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path)
    parser.add_argument("--keep", action="store_true")
    args = parser.parse_args()
    result = run(args.source, args.checkpoint, args.work_root, keep=args.keep)
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(canonical_json(result) + "\n", encoding="ascii")


if __name__ == "__main__":
    main()
