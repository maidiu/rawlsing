"""Build and observe R30G GM01 material scenarios on the real R29P product."""
from __future__ import annotations

import json
from pathlib import Path

import historical_actor_producer as H
from bp2p4 import reunion as R
from stable_actor_binding import StableJoinedProducer

from r29p.runner import stable_view
from r30g.gm01_product import GM01Product


def build(root, gm01, *, variant="A_REPAIR_LONG"):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    producer = StableJoinedProducer(root / "bp2", variant=variant)
    try:
        outcome = producer.run()
        if not outcome.ok:
            raise RuntimeError("R30G_PRODUCER_REFUSED:" + outcome.stage_reached + ":" + outcome.failure_code)
        receipt = outcome.receipt()
        persisted = receipt["persisted"]
        env = producer.env
        paths = {
            "journal_path": Path(persisted["journal_path"]),
            "key_path": env.key_path,
            "key_id": env.key_store.key_id,
            "anchor_log": env.anchor.log_path,
            "anchor_watermark": env.anchor.watermark_path,
            "c9_path": Path(persisted["c9_db_path"]),
        }
        artifacts = R._assemble(
            mode="FRESH", root=root / "bp2", life=producer.life,
            persisted=persisted, paths=paths, receipt=receipt, e2=None)
        product = GM01Product(root / "product", artifacts=artifacts,
                              variant=variant, gm01=gm01)
        return product, artifacts, producer
    except Exception:
        producer.close()
        raise


def observable(product, *, perform="e2"):
    """Frozen R30G material A0/A2 observable over the real product API."""
    a0 = product.observe_verified()
    before = a0["self"]["state"]
    if perform == "e2":
        action = product.material_inspect()
    elif perform == "omit":
        action = product.record_omission()
    elif perform == "none":
        action = {"status": "NO_CHANGE", "attempted": False,
                  "admitted": False, "reason": "NO_GM01_ACTION"}
    else:
        raise ValueError(perform)
    waited = product.wait(30)
    other = product.other()
    after = product.store.latest_state(product.branch_id)["world"]["actor_state"]["A"]
    return {
        "status": a0.get("status"),
        "claims": [claim["kind"] for claim in a0.get("claims", [])],
        "others": [row["actor"] for row in a0.get("others_present", [])],
        "tools_before": before.get("tools_remaining"),
        "material_before": before.get("material_remaining"),
        "completed_before": before.get("completed_units"),
        "action": action,
        "tools_after": after.get("tools_remaining"),
        "material_after": after.get("material_remaining"),
        "completed_after": after.get("completed_units"),
        "a2_clock": waited.get("clock"),
        "a2_offscreen": [product.store.world_event(product.branch_id, e)["kind"]
                         for e in waited.get("offscreen_events", [])],
        "a2_other_units": other["public"]["completed_units"],
        "material_start": getattr(product, "material_start_receipt", {}),
        "c12_verify": a0.get("c12_verify", {}),
    }


def stable(observed):
    return stable_view(observed)


def dump_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, sort_keys=True, default=str) + "\n",
                          encoding="utf-8")
