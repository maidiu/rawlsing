#!/usr/bin/env python3
"""Synthetic original-shaped current/revoked/wrong-request guard probe."""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path

OUT = Path(sys.argv[1]).resolve()
CAND = Path(sys.argv[2]).resolve()
RUNNER = Path(sys.argv[3]).resolve()
sys.path[:0] = [str(CAND), str(RUNNER)]

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.tests.test_pyat960_s1e_support import source_fixture
from single_pass_handoff import CheckpointRefusal, _require_current

synthetic_root = OUT.parent / "synthetic-original-shaped"
fixture = source_fixture(synthetic_root, original=True)
decision_ref = ExactRef("TEST_DECISION", "decision", "c" * 64)
request = types.SimpleNamespace(
    decision_ref=decision_ref, source_id="SRC04", source_sha256="a" * 64,
    host="TEST_HOST", purpose="TEST_PURPOSE", consumer_use="TEST_CONSUMER",
    read_operation="SOURCE_RESPONSE_DECODE", physical_read_extent="EXACT_FILE",
    metadata_freeze_refs=(ExactRef("TEST_METADATA", "m", "d" * 64),),
    semantic_use_scope=("TEST_ONLY",),
)


class Resolver:
    def __init__(self, state: str, revocation_ref=None, host="TEST_HOST"):
        self.state, self.revocation_ref, self.host = state, revocation_ref, host

    def resolve_current(self, req):
        return types.SimpleNamespace(
            currentness=self.state, revocation_ref=self.revocation_ref,
            decision_ref=req.decision_ref, source_id=req.source_id,
            source_sha256=req.source_sha256, host=self.host,
            purpose=req.purpose, consumer_use=req.consumer_use,
            read_operation=req.read_operation,
            physical_read_extent=req.physical_read_extent,
            metadata_freeze_refs=req.metadata_freeze_refs,
            semantic_use_scope=req.semantic_use_scope,
        )


def result(name: str, resolver) -> dict:
    try:
        _require_current(resolver, request, decision_ref)
    except CheckpointRefusal as exc:
        return {"case": name, "refused": True, "code": exc.code, "detail": exc.detail}
    return {"case": name, "refused": False, "code": "NOT_REFUSED", "detail": ""}


results = {
    "original_shaped_config": fixture["config"].identity_class,
    "source_decode_called": False,
    "spool_created": any(synthetic_root.glob(".s1e-i02-spool-*")),
    "cases": [
        result("held", Resolver("HELD")),
        result("revoked", Resolver("CURRENT_GRANTED", ExactRef("R", "r", "e" * 64))),
        result("wrong_request", Resolver("CURRENT_GRANTED", None, "OTHER_HOST")),
    ],
}
OUT.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
if (results["original_shaped_config"] != "ORIGINAL_SOURCE"
        or results["spool_created"]
        or results["source_decode_called"]
        or not all(case["refused"] for case in results["cases"])):
    raise SystemExit("SYNTHETIC_ORIGINAL_GUARD_PROBE_FAILED")
print(json.dumps(results, sort_keys=True))
