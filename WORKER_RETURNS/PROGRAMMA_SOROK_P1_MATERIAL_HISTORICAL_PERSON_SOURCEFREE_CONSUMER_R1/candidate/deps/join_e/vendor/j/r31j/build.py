"""Build R31J pre-C9 artifacts and the real product."""
from __future__ import annotations

from pathlib import Path

from bp2p4 import reunion as R
from r31j.pre_c9 import PreC9Producer
from r31j.product import R31JProduct


def produce(root, *, gm01, case, variant="A_REPAIR_LONG", need_e2=True):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    producer = PreC9Producer(root / "bp2", gm01=gm01, case=case, variant=variant)
    try:
        if need_e2:
            outcome = producer.run()
            if not outcome.ok:
                raise RuntimeError("R31J_PREC9_REFUSED:" + outcome.stage_reached + ":" + outcome.failure_code)
            receipt = outcome.receipt()
        else:
            partial = producer.run_without_e2()
            flat = producer._flat_receipts(producer.pipeline, None)
            receipt = {"schema": "R31J_PREC9_RECEIPT@1", "ok": True,
                       "stage_reached": "c9_commit", **flat,
                       "no_e2": True, "material_access": partial["material_access"]}
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
            mode="FRESH", root=root / "bp2", life=producer.historical_life,
            persisted=persisted, paths=paths, receipt={"persisted": persisted}, e2=None)
        return {
            "producer": producer,
            "artifacts": artifacts,
            "receipt": receipt,
            "source": producer.source,
            "c8_state_digest": persisted["c8_state_digest"],
            "e1_event_hash": persisted["e1_event_hash"],
            "target_id": persisted["target_id"],
        }
    except Exception:
        producer.close()
        raise


def product(root, *, gm01, case, variant="A_REPAIR_LONG", need_e2=True, perform="e2"):
    root = Path(root)
    built = produce(root, gm01=gm01, case=case, variant=variant, need_e2=need_e2)
    producer = built["producer"]
    artifacts = built["artifacts"]
    product_obj = R31JProduct(
        root / "product", artifacts=artifacts, source=built["source"],
        c8_state_digest=built["c8_state_digest"],
        e1_event_hash=built["e1_event_hash"],
        target_id=built["target_id"], variant=variant)
    return product_obj, built, producer


def c9_only(root, *, gm01, case, variant="A_REPAIR_LONG"):
    """Run through C9 without E2; used for lawful NO_CHANGE/refusal cases."""
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    producer = PreC9Producer(root / "bp2", gm01=gm01, case=case, variant=variant)
    try:
        return producer.run_without_e2(), producer
    except Exception:
        producer.close()
        raise
