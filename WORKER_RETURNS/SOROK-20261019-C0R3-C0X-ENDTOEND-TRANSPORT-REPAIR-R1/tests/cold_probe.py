"""Cold-process probe for the corrected C0R3 receiver."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(ROOT / "candidate"))
sys.path.insert(0, str(ROOT / "candidate" / "stage" / "runtime"))
import c0x_world_receiver as RX  # noqa: E402

SELECT = {"valid_at": "2027-09-01", "published_asof": "2027-09-01"}
PROPOSALS = [dict(scenario_id="S1", route="institutional"),
             dict(scenario_id="S2", route="civil")]


def pack(consumer):
    receipt = RX.make_receipt(
        consumer, select_kwargs=SELECT,
        proposals=PROPOSALS if consumer == "CONCEPTION_SCENARIO_PROPOSALS" else None)
    out = RX.receive_receipt(receipt, {"consumer": consumer})
    payload = json.dumps({"world_receipt": receipt.world_receipt,
                          "possibility_receipt": receipt.possibility_receipt},
                         sort_keys=True, separators=(",", ":"))
    return {
        "consumer": consumer,
        "world_fields": len(receipt.world_receipt),
        "possibility_fields": len(receipt.possibility_receipt),
        "transport": out["transport"]["state"],
        "json_serializable": out["transport"]["json_serializable"],
        "parent0": receipt.possibility_receipt["ordered_steps"][0]["parent_receipt_ref"],
        "owner_receipt_hash": receipt.owner_receipt_hash,
        "selection": len(receipt.world_receipt["selection"]),
        "ordered_steps": len(receipt.possibility_receipt["ordered_steps"]),
        "values_read": len(out["values_read"] or []),
        "json_sha256": hashlib.sha256(payload.encode()).hexdigest(),
        "evidence_state": out["evidence_state"],
    }


print(json.dumps({"nonparent": pack("NONPARENT_OPTIONS"),
                  "conception": pack("CONCEPTION_SCENARIO_PROPOSALS")},
                 sort_keys=True))
