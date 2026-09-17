#!/usr/bin/env python3
"""Execute the accepted banked LiTS projection and print only its identity receipt."""
from __future__ import annotations

import json
from pathlib import Path

from rawlsing_next.pre553_as4i0_route_b_driver import build_route_b_source_session

BANKED_ROOT = Path("/tmp/rawlsing-ee-r10l-banked")
SOURCE = Path("/Users/matthewsmith/Desktop/Rawlsing/data/LiTS/LITS-2006-data.dta")
BASE = BANKED_ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827"

session = build_route_b_source_session(SOURCE, BASE / "banked_as2b/run_as2b_lits1_mechanical_certification.py", BASE / "banked_as2a")
try:
    receipt = {
        "source_sha256": session.source_sha256,
        "projection_cache_identity": session.projection_hash,
        "c11_logical_release": session.release.semantic_release_hash,
        "as2b_replay_manifest": session.replay_manifest_hash,
        "repository_snapshot_hash": session.repository_snapshot_hash,
    }
    assert receipt["projection_cache_identity"] == "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
    assert receipt["c11_logical_release"] == "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
    assert receipt["as2b_replay_manifest"] == "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
    print(json.dumps(receipt, sort_keys=True))
finally:
    session.close()
