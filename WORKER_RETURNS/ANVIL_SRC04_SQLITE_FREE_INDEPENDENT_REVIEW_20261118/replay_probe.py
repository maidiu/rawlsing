#!/usr/bin/env python3
"""Minimal sourcefree replay: exercise the new proof boundary and probe actual
operator-consumer obligations without changing any code."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1]).resolve()
CAND = Path(sys.argv[2]).resolve()
CUT = Path(sys.argv[3]).resolve()
WORK = Path(sys.argv[4]).resolve()
sys.path[:0] = [str(CUT), str(CAND), str(WORK)]

from streaming_estate import open_stream_native_estate, write_streaming_estate
from test_streaming_cut import _sections

work = OUT.parent / "replay-work"
work.mkdir(parents=True, exist_ok=True)
p, universe_ref, root, make = _sections(work)
newroot = root / "stream"
newroot.mkdir(mode=0o700)
progress = []
receipt = write_streaming_estate(make(), universe_ref, newroot, chunk_rows=2, progress=progress.append)
estate = open_stream_native_estate(
    newroot, receipt.path, receipt.manifest_sha256, receipt.roots,
    current_authorizer=lambda roots: True, progress=progress.append,
)
counts = {family: sum(1 for _ in estate.iter_family(family, batch_size=2))
          for family in receipt.family_counts}
reader_attr = {
    "has_legacy_i02_attr": hasattr(receipt, "i02"),
    "has_roots_attr": hasattr(receipt, "roots"),
    "reconstructed_v1_release_ref": repr(estate.reconstructed_v1_release_ref),
}
try:
    reader_attr["reconstructed_release_as_dict"] = estate.reconstructed_v1_release_ref.as_dict()
except Exception as exc:
    reader_attr["reconstructed_release_as_dict"] = {
        "raised": type(exc).__name__, "message": str(exc)
    }
proof = {
    "schema": "ANVIL_SRC04_SQLITE_FREE_NATIVE_REPLAY@1",
    "sourcefree_test_only": True,
    "original_source_read": False,
    "receipt_type": type(receipt).__name__,
    "receipt_fields": sorted(k for k in vars(receipt)),
    "reader_type": type(estate).__name__,
    "counts": counts,
    "progress_phases": [p.get("phase") for p in progress],
    "reader_attr": reader_attr,
    "manifest_schema": estate.manifest.get("schema"),
    "no_sqlite_file": not any(p.suffix == ".sqlite" for p in newroot.rglob("*")),
}
OUT.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
print(json.dumps(proof, sort_keys=True))
