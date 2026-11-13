#!/usr/bin/env python3
from __future__ import annotations
import json, os, sys, tempfile
from pathlib import Path
ROOT = Path(os.environ.get('Q2_PROBE_ROOT', Path(__file__).resolve().parents[2]))
sys.path.insert(0, str(ROOT))
from rawlsing_next.tests.test_pyat960_s1e_support import build, source_fixture

def main():
    root = Path(tempfile.mkdtemp(prefix="q2-multiowner-"))
    fixture = source_fixture(
        root / "multiowner", routing_state="ROUTING_UNKNOWN",
        config_kwargs={"duplicate_slot_owner": True, "include_slot_owner_set": True})
    try:
        handoff = build(root / "multiowner", fixture, name="out.sqlite")
        print(json.dumps({"accepted": True, "counts": dict(handoff.counts),
                          "audit": dict(handoff.census_audit["operation_source_antijoin"])}, indent=2))
    except Exception as exc:
        print(json.dumps({"accepted": False, "error": type(exc).__name__, "detail": str(exc)}, indent=2))
    return 0
raise SystemExit(main())
