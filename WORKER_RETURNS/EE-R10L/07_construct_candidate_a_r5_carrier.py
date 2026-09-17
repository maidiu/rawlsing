#!/usr/bin/env python3
"""Execute the measured Route-A R5 compact-carrier construction for EE-R10L."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import platform
import resource
import threading
import time
from pathlib import Path
from typing import Any


SOURCE_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
PROJECTION = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
C11 = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
REPLAY = "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree(path: Path) -> tuple[int, int, int]:
    total = files = maximum = 0
    if not path.exists():
        return total, files, maximum
    for root, _dirs, names in os.walk(path):
        for name in names:
            try:
                size = (Path(root) / name).stat().st_size
            except OSError:
                continue
            total += size
            files += 1
            maximum = max(maximum, size)
    return total, files, maximum


class Monitor:
    def __init__(self, root: Path):
        self.root = root
        self.stop = threading.Event()
        self.peak_bytes = self.peak_files = self.max_file = 0
        self.thread = threading.Thread(target=self.run, daemon=True)

    def sample(self) -> None:
        value, files, maximum = tree(self.root)
        self.peak_bytes = max(self.peak_bytes, value)
        self.peak_files = max(self.peak_files, files)
        self.max_file = max(self.max_file, maximum)

    def run(self) -> None:
        while not self.stop.wait(0.25):
            self.sample()
        self.sample()

    def start(self) -> None:
        self.sample()
        self.thread.start()

    def close(self) -> None:
        self.stop.set()
        self.thread.join(timeout=5)
        self.sample()


def load_builder(path: Path):
    import rawlsing_next.pre553_c11_ingest  # noqa: F401
    import rawlsing_next.pre553_c11_integrity  # noqa: F401
    import rawlsing_next.pre553_c11_repository  # noqa: F401
    import rawlsing_next.pre553_empirical_authority  # noqa: F401
    import rawlsing_next.pre553_empirical_objects  # noqa: F401
    import rawlsing_next.pre553_empirical_query  # noqa: F401
    import rawlsing_next.pre553_physical_decoder  # noqa: F401
    import rawlsing_next.pre553_source_backed_c11_facade  # noqa: F401
    spec = importlib.util.spec_from_file_location("ee_r10l_a_banked_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load accepted banked AS2B builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PART_A_DIR = path.parent.parent / "banked_as2a"
    module.LEDGER = module.PART_A_DIR / "01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"
    module.PACKAGE = module.PART_A_DIR / "04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--builder", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    from rawlsing_next.pre553_c11_ingest import validate_c11_source_release
    from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedBuilder
    from rawlsing_next.pre553_r5_model import R5ReleaseIdentity
    from rawlsing_next.pre553_r5_seam import iter_source_native_rows

    source = Path(args.source)
    target = Path(args.target)
    if target.exists():
        raise RuntimeError("Route-A target must be absent; no prebuilt carrier may be reused")
    builder = load_builder(Path(args.builder))
    if builder.sha256_file(source) != SOURCE_SHA:
        raise RuntimeError("exact LiTS-I source SHA mismatch")

    started_wall = time.monotonic_ns()
    started_cpu = time.process_time_ns()
    incidence = builder.decode_dta(source, encoding="latin1")
    package, ledger, slots = builder.read_banked_authority()
    projection, _context = builder.build_projection(incidence, package, ledger, slots)
    if projection.cache_identity != PROJECTION:
        raise RuntimeError("banked projection cache identity mismatch")
    selected_names = ("country", "city", "region", "q301_2", "q301_7", "tablec", "tabled")
    variables = tuple(v for v in incidence.variables if v.name in selected_names)
    selected = builder.PhysicalSourceIncidence(
        source_sha256=incidence.source_sha256,
        source_format=incidence.source_format,
        row_count=incidence.row_count,
        variables=variables,
        reader_configuration={**incidence.reader_configuration, "transport": "EE_R10L_ROUTE_A_RELEASE_IDENTITY"},
        file_metadata=incidence.file_metadata,
        _frame=incidence._frame[[v.name for v in variables]],
    )
    candidate = builder.project_c11_candidate_from_physical_cells(
        source_sha256=SOURCE_SHA,
        row_count=builder.ROWS,
        cells=(builder.exact_cell(cell) for cell in selected.iter_cells(batch_size=20_000)),
        projection=projection,
    )
    release = validate_c11_source_release(candidate)
    if release.semantic_release_hash != C11 or release.replay_manifest.content_hash != REPLAY:
        raise RuntimeError("Route-A release identity inputs diverge from accepted C11/replay")
    identity = R5ReleaseIdentity(
        release_id=release.release_id,
        semantic_release_hash=release.semantic_release_hash,
        source_artifact_ref=release.source_artifact_ref.as_dict(),
        source_release_manifest_hash=release.source_release_manifest_hash,
        m01_m18_coverage={key: tuple(value) for key, value in release.m01_m18_coverage.items()},
        decoder_receipt={
            "source_sha256": SOURCE_SHA,
            "decoder": "decode_dta(source_path, encoding=latin1)",
            "pyreadstat": "1.3.6",
            "physical_cells": 34_744_396,
        },
        compiler_contract_digest=file_sha(Path(args.builder)),
        c11_authority_digest=PROJECTION,
    )
    monitor = Monitor(target.parent)
    monitor.start()
    before_bytes, _before_files, _before_max = tree(target.parent)
    try:
        telemetry = R5CompactLongShardedBuilder().build(
            iter_source_native_rows(incidence, batch_size=10_000),
            release_identity=identity,
            target_directory=target,
        )
    finally:
        monitor.close()
    after_bytes, after_files, after_max = tree(target.parent)
    usage = resource.getrusage(resource.RUSAGE_SELF)
    rss_native = int(usage.ru_maxrss)
    rss_bytes = rss_native if platform.system() == "Darwin" else rss_native * 1024
    result = {
        "schema": "RAWLSING_EE_R10L_CANDIDATE_A_R5_CONSTRUCTION_RECEIPT@1.0.0",
        "status": "PASS__MEASURED_ROUTE_A_R5_LONG_COMPACT_CARRIER_CONSTRUCTED",
        "candidate": "A",
        "candidate_execution_order_position": 1,
        "physical_meaning": "R5_LONG_COMPACT_V2__SERIAL_V4__AUDIT69__C05R2A_FACADE",
        "source": {"sha256": SOURCE_SHA, "rows": 29_002, "variables": 1_198, "physical_cells": 34_744_396, "decoder": "decode_dta(source_path, encoding=latin1)", "pyreadstat": "1.3.6"},
        "projection_cache_identity": PROJECTION,
        "c11_logical_release": C11,
        "as2b_replay_manifest": REPLAY,
        "carrier": {"target": str(target), "exists": target.is_dir(), "telemetry": telemetry},
        "w4_telemetry": {
            "wall_ns": time.monotonic_ns() - started_wall,
            "cpu_user_ns": int(usage.ru_utime * 1_000_000_000),
            "cpu_system_ns": int(usage.ru_stime * 1_000_000_000),
            "peak_rss_native": rss_native,
            "peak_rss_native_unit": "bytes" if platform.system() == "Darwin" else "KiB",
            "peak_rss_bytes": rss_bytes,
            "scratch_bytes_before": before_bytes,
            "scratch_bytes_after": after_bytes,
            "peak_scratch_bytes_observed": monitor.peak_bytes,
            "peak_scratch_file_count_observed": monitor.peak_files,
            "max_single_temp_object_bytes_observed": monitor.max_file,
            "durable_bytes_before": 0,
            "durable_bytes_after": telemetry["canonical_steady_state_bytes"],
            "durable_bytes_created_delta": telemetry["canonical_steady_state_bytes"],
            "source_open_count": 1,
            "source_decode_count": 1,
            "bytes_read": source.stat().st_size,
            "bytes_written": telemetry["canonical_steady_state_bytes"],
            "temporary_spill_bytes_reported": None,
            "cache_index_bytes_created": None,
            "rewritten_bytes": telemetry["canonical_steady_state_bytes"],
            "semantic_oracle_status": "NOT_YET_APPLIED__C11_ADAPTER_STAGE_PENDING",
            "identity_oracle_status": "PASS__BANKED_C11_RELEASE_AND_REPLAY_BOUND",
        },
        "runtime": {"python": platform.python_version(), "pyreadstat": "1.3.6", "pyarrow": "25.0.1", "darwin_peak_rss_normalization": platform.system() == "Darwin"},
        "no_rank_or_policy_decision": True,
    }
    Path(args.out).write_bytes(canonical(result))
    print(json.dumps({"status": result["status"], "physical_root_id": telemetry["physical_root_id"], "steady_state_bytes": telemetry["canonical_steady_state_bytes"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
