#!/usr/bin/env python3
"""Honest Q2 S1-E small-fixture resource receipt (not 100k / 6 GiB).

Measures one-source-read body-preserving handoff, certificate retention, spool
scratch, process RSS, cold/repeat, and actual decoder/source-open counts.
"""
from __future__ import annotations

import hashlib
import json
import resource
import shutil
import sys
import tempfile
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import rawlsing_next.pre553_physical_decoder as decoder  # noqa: E402
import rawlsing_next.pre553_source_i02_handoff as handoff_module  # noqa: E402
from rawlsing_next.pre553_empirical_objects import semantic_hash  # noqa: E402
from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES  # noqa: E402
from rawlsing_next.tests.test_pyat960_s1e_support import (  # noqa: E402
    build,
    source_fixture,
)


def _rss() -> int:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == "darwin" else value * 1024


class CountingSink:
    def __init__(self):
        self.counts: Counter[str] = Counter()
        self.absences: dict[str, str] = {}
        self.objects = 0
        self.finished = False
        self.aborted = False
        self.roots = None
        self.manifest = None
        self.transport = None

    def begin(self, **kwargs):
        self.begin = kwargs

    def emit(self, family, obj):
        assert type(obj).__name__ == family
        assert semantic_hash(obj.semantic_projection()) == obj.ref.content_hash
        self.counts[family] += 1
        self.objects += 1

    def absence(self, family, absence):
        self.absences[family] = absence.state

    def finish(self, **kwargs):
        self.roots = kwargs["roots"]
        self.manifest = kwargs["manifest"]
        self.transport = kwargs["transport"]
        self.finished = True

    def abort(self, exc):
        self.aborted = True


def main() -> int:
    proof = Path(tempfile.mkdtemp(prefix="pyat960-q2-b-resource-"))
    try:
        fixture = source_fixture(
            proof,
            values=tuple(float(index % 4) for index in range(1200)),
            policy_kwargs={"j": 1, "k": 1, "d": 0},
        )
        source_bytes = fixture["path"].stat().st_size

        actual = {"snapshot": 0, "sha": 0, "decode": 0, "builder": 0}
        original_snapshot = decoder._acquire_source_snapshot
        original_sha = decoder._sha
        original_decode_sav = handoff_module.decode_sav
        original_decode_dta = handoff_module.decode_dta
        original_builder = handoff_module.build_sourcefree_direct_i02

        def snapshot(*args, **kwargs):
            actual["snapshot"] += 1
            return original_snapshot(*args, **kwargs)

        def sha(*args, **kwargs):
            actual["sha"] += 1
            return original_sha(*args, **kwargs)

        def decode_sav(*args, **kwargs):
            actual["decode"] += 1
            return original_decode_sav(*args, **kwargs)

        def decode_dta(*args, **kwargs):
            actual["decode"] += 1
            return original_decode_dta(*args, **kwargs)

        def builder(*args, **kwargs):
            actual["builder"] += 1
            return original_builder(*args, **kwargs)

        decoder._acquire_source_snapshot = snapshot
        decoder._sha = sha
        handoff_module.decode_sav = decode_sav
        handoff_module.decode_dta = decode_dta
        handoff_module.build_sourcefree_direct_i02 = builder
        try:
            baseline = _rss()
            cold_sink = CountingSink()
            cold_start = time.perf_counter()
            cold = build(
                proof,
                fixture,
                name="cold.sqlite",
                body_sink=cold_sink,
            )
            cold_seconds = time.perf_counter() - cold_start
            cold_actual = dict(actual)
            actual.update({key: 0 for key in actual})
            cold_certificate_bytes = Path(cold.destination).stat().st_size
            spool_bytes = cold.stats.spool_bytes
            fixture_bytes = source_bytes
            cold_peak_disk_bytes = (
                fixture_bytes + spool_bytes + cold_certificate_bytes)
            cold_rss = _rss()

            repeat_sink = CountingSink()
            repeat_start = time.perf_counter()
            repeat = build(
                proof,
                fixture,
                name="repeat.sqlite",
                body_sink=repeat_sink,
            )
            repeat_seconds = time.perf_counter() - repeat_start
            repeat_actual = dict(actual)
            repeat_certificate_bytes = Path(repeat.destination).stat().st_size
            repeat_spool_bytes = repeat.stats.spool_bytes
            repeat_peak_disk_bytes = (
                fixture_bytes + cold_certificate_bytes
                + repeat_spool_bytes + repeat_certificate_bytes
            )
            peak_disk_bytes = max(cold_peak_disk_bytes, repeat_peak_disk_bytes)
            repeat_rss = _rss()
        finally:
            decoder._acquire_source_snapshot = original_snapshot
            decoder._sha = original_sha
            handoff_module.decode_sav = original_decode_sav
            handoff_module.decode_dta = original_decode_dta
            handoff_module.build_sourcefree_direct_i02 = original_builder

        manifest_counts = {
            family: cold.manifest.declared_record_counts_by_logical_family[family]
            for family in ALL_FAMILIES
        }
        observed_counts = {
            family: cold_sink.counts.get(family, 0) for family in ALL_FAMILIES
        }
        assert observed_counts == manifest_counts
        assert cold_sink.finished is True
        assert cold_sink.transport["complete"] is True
        assert cold.roots == cold_sink.roots
        assert cold.manifest.content_hash == cold_sink.manifest.content_hash
        assert cold.roots.logical == repeat.roots.logical
        assert cold.roots.physical == repeat.roots.physical

        # Measure actual retained custody: remove the repeat certificate and the
        # generated source fixture, keep the cold certificate as the retained
        # output.  This reconciles A's retained_disk_bytes=0 conflict without
        # rewriting A's historical evidence.
        Path(repeat.destination).unlink()
        fixture["path"].unlink(missing_ok=True)
        for path in fixture["path"].parent.glob("*"):
            if path.is_file():
                path.unlink(missing_ok=True)
        retained_disk_bytes = cold_certificate_bytes
        result = {
            "rows": cold.stats.source_rows,
            "events": cold.stats.event_count,
            "coordinates": cold.stats.coordinate_count,
            "weights": cold.stats.weight_count,
            "body_transport": {
                "schema": cold.body_transport["schema"],
                "families": dict(cold.body_transport["families"]),
                "absences": dict(cold.body_transport["absences"]),
                "empty_families": list(cold.body_transport["empty_families"]),
                "object_count": cold.body_transport["object_count"],
                "complete": cold.body_transport["complete"],
                "finished": cold.body_transport["finished"],
            },
            "actual_counts": {
                "scope": "cold build only",
                "snapshot_acquisitions": cold_actual["snapshot"],
                "source_prehash_passes": cold_actual["sha"],
                "source_byte_passes": cold_actual["snapshot"] + cold_actual["sha"],
                "decode_calls": cold_actual["decode"],
                "direct_builder_calls": cold_actual["builder"],
                "cell_passes": cold.stats.cell_passes,
                "key_witness_passes": cold.stats.key_witness_passes,
                "full_c11_builds": cold.stats.full_c11_builds,
            },
            "repeat_actual_counts": {
                "scope": "repeat build only",
                "snapshot_acquisitions": repeat_actual["snapshot"],
                "source_prehash_passes": repeat_actual["sha"],
                "source_byte_passes": (
                    repeat_actual["snapshot"] + repeat_actual["sha"]),
                "decode_calls": repeat_actual["decode"],
                "direct_builder_calls": repeat_actual["builder"],
            },
            "reported_stats": cold.stats.__dict__,
            "source_open_model": cold.stats.source_open_model,
            "source_fixture_bytes": fixture_bytes,
            "spool_bytes": spool_bytes,
            "spool_files": cold.stats.spool_files,
            "spool_cleanup_glob": [
                str(path) for path in proof.glob(".s1e-i02-spool-*")
            ],
            "cold_certificate_bytes": cold_certificate_bytes,
            "repeat_certificate_bytes": repeat_certificate_bytes,
            "repeat_spool_bytes": repeat_spool_bytes,
            "retained_disk_bytes_after_cleanup": retained_disk_bytes,
            "peak_disk_bytes": peak_disk_bytes,
            "scratch_bytes": spool_bytes,
            "baseline_process_rss_bytes": baseline,
            "cold_process_rss_bytes": cold_rss,
            "repeat_process_rss_bytes": repeat_rss,
            "peak_process_rss_bytes": max(cold_rss, repeat_rss),
            "cold_seconds": cold_seconds,
            "repeat_seconds": repeat_seconds,
            "platform": sys.platform,
            "budget_result": (
                "SMALL_SOURCEFREE_FIXTURE; 100k RESPONDENT / 6GiB INTEGRATED "
                "GATE NOT_RUN; Q2 DOES NOT CLAIM S2-C/S2-D ECONOMICS"
            ),
            "host_native_first_reader": (
                "HOLD_DEPENDENCY: VerifiedExternalI02 requires Linux "
                "/proc/self/fd and a sealed body release; not run on Darwin"
            ),
        }
        print(json.dumps(result, indent=2, sort_keys=True))
    finally:
        shutil.rmtree(proof, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
