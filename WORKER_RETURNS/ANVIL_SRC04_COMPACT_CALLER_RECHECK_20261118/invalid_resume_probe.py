#!/usr/bin/env python3
"""Sourcefree invalid resume without any source path: missing checkpoint refuses."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1]).resolve()
ROOT = Path(sys.argv[2]).resolve()
CAND = Path(sys.argv[3]).resolve()
RUNNER = Path(sys.argv[4]).resolve()
sys.path[:0] = [str(CAND), str(RUNNER)]

from compact_rehearsal import fixture, req
from single_pass_handoff import CheckpointRefusal, resume_single_pass

cfg, _source_path = fixture(ROOT)
request, grant_ref, decision_ref = req(cfg)
private = ROOT / "invalid-private"
private.mkdir(mode=0o700, exist_ok=True)
missing = private / "missing.checkpoint.json"
try:
    resume_single_pass(
        checkpoint=missing, root=private, config=cfg, request=request,
        grant_ref=grant_ref, decision_ref=decision_ref, chunk_rows=2,
    )
except CheckpointRefusal as exc:
    proof = {
        "schema": "ANVIL_SRC04_SOURCEFREE_INVALID_RESUME@1",
        "refused": True,
        "code": exc.code,
        "detail": exc.detail,
        "source_path_supplied": False,
        "source_decode_called": False,
        "publication_started": False,
    }
    OUT.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
    print(json.dumps(proof, sort_keys=True))
else:
    raise SystemExit("MISSING_CHECKPOINT_WAS_NOT_REFUSED")
