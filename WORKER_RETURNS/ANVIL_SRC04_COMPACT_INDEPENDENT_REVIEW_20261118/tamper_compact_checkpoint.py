#!/usr/bin/env python3
"""One decisive compact checkpoint spool-corruption refusal on a disposable copy."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
P = Path(__file__).resolve().parents[2]  # OWNER/WORKER_RETURNS/... -> OWNER
# The rehearsal script and exact candidate tree are supplied by env.
CAND = Path(sys.argv[3]).resolve()
RUNNER = Path(sys.argv[4]).resolve()
sys.path.insert(0, str(CAND))
sys.path.insert(0, str(RUNNER))
from compact_rehearsal import fixture, req
from single_pass_handoff import resume_single_pass, CheckpointRefusal

compact_private = ROOT / "compact-private"
tamper_private = ROOT / "tamper-private"
shutil.copytree(compact_private, tamper_private)
spool_files = sorted(tamper_private.glob(".s1e-i02-spool-*/*.jsonl.gz"))
if not spool_files:
    raise SystemExit("NO_COMPACT_SPOOL_FOR_TAMPER")
victim = next(path for path in spool_files if path.stat().st_size > 0)
raw = bytearray(victim.read_bytes())
raw[len(raw) // 2] ^= 0x01
victim.write_bytes(raw)
cfg, path = fixture(ROOT)
request, grant_ref, decision_ref = req(cfg)
checkpoint = tamper_private / "prepared-sections.checkpoint.json"
refused = False
code = ""
detail = ""
try:
    resume_single_pass(
        checkpoint=checkpoint, root=tamper_private, config=cfg,
        request=request, grant_ref=grant_ref, decision_ref=decision_ref,
        chunk_rows=2,
    )
except CheckpointRefusal as exc:
    refused = True
    code = exc.code
    detail = exc.detail
proof = {
    "schema": "ANVIL_SRC04_COMPACT_CORRUPTION_REFUSAL@1",
    "refused": refused,
    "error_type": "CheckpointRefusal",
    "code": code,
    "detail": detail,
    "tampered_file": victim.name,
    "tampered_bytes": len(raw),
    "checkpoint_present_before": checkpoint.is_file(),
    "source_decode_called": False,
    "publication_started": False,
}
OUT.write_text(json.dumps(proof, indent=2, sort_keys=True) + "\n")
if not refused:
    raise SystemExit("CORRUPTION_WAS_NOT_REFUSED")
print(json.dumps(proof, sort_keys=True))
