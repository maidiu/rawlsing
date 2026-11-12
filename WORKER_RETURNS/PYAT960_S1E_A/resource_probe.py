#!/usr/bin/env python3
"""Honest small Q2 sourcefree resource receipt; no 100k/full-matrix claim."""
from __future__ import annotations
import json, resource, sys, tempfile, time
from dataclasses import replace
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from rawlsing_next.pre553_r157_projection_adapter import SourceConfig
from rawlsing_next.pre553_source_i02_handoff import build_source_i02_handoff
from rawlsing_next.tests.test_pyat940_s1b_support import make_config, write_fixture
from rawlsing_next.tests.test_pyat_r3_s1c_source_operation_fates import _freeze_packet
from rawlsing_next.tests.test_universal_grammar import _inventory, _occurrence, _policy, _frontier

root = Path(tempfile.mkdtemp(prefix="pyat960-q2-resource-"))
values = tuple(float(index % 3) for index in range(1200))
path, sha, rows = write_fixture(root / "src", source_format="SAV", values=values)
document = make_config(source_format="SAV", active_source_sha256=sha, row_count=rows, values=values, keyed=False)
config = SourceConfig(document)
inventory = replace(
    _inventory((_occurrence("q101"),), complete=True),
    source_id=document["identity"]["source_id"], wave=document["identity"]["wave"],
    edition=document["identity"]["instrument_release_id"], source_sha256=sha,
    inventory_id="PYAT960-Q2-RESOURCE",
)
policy = _policy(j=2, k=2, d=1)
frontier = _frontier(inventory, policy)
census = _freeze_packet(frontier)
baseline = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
t0 = time.perf_counter()
handoff = build_source_i02_handoff(
    config=config, source_path=path, destination=root / "i02.sqlite",
    census=census, inventory=inventory, policy=policy, frontier=frontier,
)
cold = time.perf_counter() - t0
t1 = time.perf_counter()
# Repeat the same direct build (new destination) to record a second-process measure.
handoff2 = build_source_i02_handoff(
    config=config, source_path=path, destination=root / "i02-repeat.sqlite",
    census=census, inventory=inventory, policy=policy, frontier=frontier,
)
repeat = time.perf_counter() - t1
result = {
    "rows": handoff.row_count,
    "source_reads": handoff.stats.source_reads,
    "cell_passes": handoff.stats.cell_passes,
    "full_c11_builds": handoff.stats.full_c11_builds,
    "events": handoff.stats.event_count,
    "coordinates": handoff.stats.coordinate_count,
    "weights": handoff.stats.weight_count,
    "spool_bytes": handoff.stats.spool_bytes,
    "spool_files": handoff.stats.spool_files,
    "certificate_bytes": Path(handoff.destination).stat().st_size,
    "root_logical": handoff.roots.logical,
    "root_physical": handoff.roots.physical,
    "deterministic_repeat": handoff.roots.logical == handoff2.roots.logical,
    "baseline_process_rss_bytes": baseline,
    "peak_process_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    "cold_seconds": cold,
    "repeat_seconds": repeat,
    "platform": sys.platform,
    "retained_disk_bytes": 0,
    "spool_cleanup_glob": list(root.glob(".s1e-i02-spool-*")),
}
print(json.dumps(result, indent=2, sort_keys=True))
