"""Independent fixture-grade resource and base-positive receipt for PYAT960 S2-G.

Uses the existing synthetic M01/M1/M2/B5 fixture and the actual world consumer.
Writes only to the caller-supplied private proofroot.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import resource
import sys
import time

from rawlsing_next.tests.test_pyat960_s2g_durable_lifecycle import _artifact_case


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        raise SystemExit("usage: repro_resources.py <private-proofroot>")
    proofroot = Path(argv[1]).resolve()
    proofroot.mkdir(parents=True, exist_ok=True)
    item = _artifact_case(proofroot / "base")
    artifact = item["artifact"]
    root = Path(artifact.artifact_path).parent.parent
    files = [path for path in root.rglob("*") if path.is_file()]
    retained = sum(path.stat().st_size for path in files)
    compressed = item["published"].compressed_bytes
    manifest = item["published"].manifest_bytes
    opens: list[str] = []

    def _audit(event, args):
        if event != "open" or not args:
            return
        text = str(args[0]).lower()
        if text.endswith((".sav", ".dta", ".parquet", ".csv", ".rdata", ".rds")):
            opens.append(text)

    sys.addaudithook(_audit)
    started = time.monotonic()
    first = artifact.consume(item["s2f_receipt"].root_path)
    cold = time.monotonic() - started
    repeat_started = time.monotonic()
    second = artifact.consume(item["s2f_receipt"].root_path)
    repeat = time.monotonic() - repeat_started
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    max_rss_bytes = int(max_rss) if sys.platform == "darwin" else int(max_rss) * 1024
    evidence = {
        "artifact_root_identity": artifact.root_identity,
        "s2f_root_identity": item["s2f_receipt"].root_identity,
        "consumer_state": first.state,
        "consumer_result_hash": first.consumer_result_hash,
        "consumer_matches_repeat": first.consumer_result_hash == second.consumer_result_hash,
        "retained_disk_bytes": retained,
        "compressed_blob_bytes": compressed,
        "manifest_bytes": manifest,
        "logical_bytes": item["published"].logical_bytes,
        "cold_seconds": cold,
        "repeat_seconds": repeat,
        "process_tree_peak_rss_bytes": max_rss_bytes,
        "source_opens": len(opens),
        "source_open_candidates": opens[:20],
        "artifact_files": len(files),
        "cap_bytes": 6 * 1024**3,
        "cap_result": "PASS" if max_rss_bytes < 6 * 1024**3 else "FAIL",
        "integrated_100k": "NOT_RUN",
    }
    (proofroot / "s2g_resource_evidence.json").write_text(
        json.dumps(evidence, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0 if first.state == "LEARNED_CONSUMER_EXACT_SUPPORTED" and not opens else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
