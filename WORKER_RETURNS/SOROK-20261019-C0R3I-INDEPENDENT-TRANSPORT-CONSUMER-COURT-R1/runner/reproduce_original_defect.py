#!/usr/bin/env python3
"""Reproduce the inherited C0X/C0P defect against the exact original receiver."""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT))
import c0x_world_receiver as RX  # noqa: E402

SELECT = {"valid_at": "2027-09-01", "published_asof": "2027-09-01"}
EARLY = {"valid_at": "2026-02-01", "published_asof": "2026-02-01"}

receipt = RX.make_receipt("NONPARENT_OPTIONS", select_kwargs=SELECT)
parent = receipt.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"]
try:
    json.dumps(receipt.possibility_receipt)
    json_error = None
except Exception as exc:  # expected TypeError
    json_error = {"type": type(exc).__name__, "message": str(exc)}
out = RX.receive_receipt(receipt, {"consumer": "NONPARENT_OPTIONS"})
temporal = None
try:
    RX.make_receipt("NONPARENT_OPTIONS", select_kwargs=EARLY)
except Exception as exc:
    temporal = {"type": type(exc).__name__, "message": str(exc),
                "traceback_last_line": traceback.format_exc().strip().splitlines()[-1]}
payload = {
    "schema": "SOROK_C0R3_INHERITED_DEFECT_REPRODUCTION@1",
    "original_c0x_root": ROOT.name,
    "original_parent_ref": {
        "path": "possibility_receipt.ordered_steps[0].parent_receipt_ref",
        "type": type(parent).__name__,
        "callable": callable(parent),
        "qualname": getattr(parent, "__qualname__", None),
    },
    "possibility_json_error": json_error,
    "receiver_transport": out["transport"],
    "temporal_early_clock": temporal,
}
print(json.dumps(payload, sort_keys=True, indent=2))
