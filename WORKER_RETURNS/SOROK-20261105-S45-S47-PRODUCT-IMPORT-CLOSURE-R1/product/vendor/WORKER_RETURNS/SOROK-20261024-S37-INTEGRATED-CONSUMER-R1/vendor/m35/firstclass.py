"""First-class BP2 B-source builder over the warm R31J/JOIN-E closure.

The source is constructed from the actual performed B observation in the GM01
case, validated by ``bp2_joined.material_source``, and passed into the BP2
producer before ``stage_world``/C8. A's tool state is derived from the performed
operation and quantity; the caller's ``gm01.material_feasible_after`` boolean is
not used for that state.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from pathlib import Path

from bp1.canon import digest, seal
import historical_actor_producer as H
from bp2p4 import reunion as R
from bp2_joined import JoinedProducer, validate_material_source
from bp2_joined.material_source import (
    MaterialSourceRefusal,
    SHARE_TOOL,
    material_access,
)
from r31j.product import R31JProduct


PREIMAGE_FIELDS = (
    "b_actor", "b_owner", "b_event_ref", "b_event_hash", "b_performed",
    "b_operation", "b_quantity", "b_to_actor", "b_clock",
    "a_e1_ref", "a_e1_hash", "a_e1_clock",
)


def case_preimage(case: dict) -> dict:
    """Return the exact observed B and A E1 fields that a source must match."""
    b_event = next(r for r in case["records"] if r["kind"] == "OTHER_PERFORMED")
    e1 = next(r for r in case["records"] if r["kind"] == "E1_EVENT")
    return {
        "b_actor": b_event["subject"],
        "b_owner": b_event["owner"],
        "b_event_ref": b_event["ref"],
        "b_event_hash": b_event["content_hash"],
        "b_performed": bool(b_event["performed"]),
        "b_operation": b_event["payload"].get("operation"),
        "b_quantity": int(b_event["payload"].get("quantity", 0)),
        "b_to_actor": b_event["payload"].get("to_actor"),
        "b_clock": int(b_event["at"]),
        "a_e1_ref": e1["ref"],
        "a_e1_hash": e1["content_hash"],
        "a_e1_clock": int(e1["at"]),
    }


def source_from_case(case: dict) -> dict:
    """Project the exact GM01 B/E1 preimage into the first-class BP2 envelope."""
    return {
        "schema": "BP2_FIRSTCLASS_B_MATERIAL_SOURCE@1",
        **case_preimage(case),
        "source_grade": "TEST_ONLY_SOURCEFREE",
        "native": False,
        "psychology_claim": False,
    }


def validate_source(source: dict, case: dict) -> dict:
    """Require the exact B and E1 preimage, not merely a valid-looking envelope."""
    normalized = validate_material_source(source)
    expected = case_preimage(case)
    for field in PREIMAGE_FIELDS:
        if normalized[field] != expected[field]:
            raise MaterialSourceRefusal(
                "MATERIAL_SOURCE_PREIMAGE_MISMATCH",
                f'{field}: {normalized[field]!r} != {expected[field]!r}')
    return normalized


def prepare_life(source: dict, variant: str = "A_REPAIR_LONG"):
    """Derive A's material tool state from B's performed operation/quantity."""
    life = H.build_life(variant)
    snapshot = deepcopy(life.a_snapshot)
    snapshot["state"] = dict(snapshot["state"])
    snapshot["state"]["tools_remaining"] = (
        1 if material_access(source) == "granted" else 0)
    snapshot["state"]["material_remaining"] = max(
        4, int(snapshot["state"].get("material_remaining", 4)))
    snapshot.pop("hash", None)
    snapshot["state_hash"] = digest(snapshot["state"])
    snapshot = seal(snapshot)
    return replace(life, a_snapshot=snapshot)


def _producer(root: Path, source: dict, variant: str) -> JoinedProducer:
    return JoinedProducer(
        Path(root) / "bp2",
        material_source=source,
        life=prepare_life(source, variant),
    )


def _persisted(producer: JoinedProducer, receipt: dict) -> tuple[dict, dict]:
    persisted = receipt["persisted"]
    paths = {
        "journal_path": Path(persisted["journal_path"]),
        "key_path": producer.env.key_path,
        "key_id": producer.env.key_store.key_id,
        "anchor_log": producer.env.anchor.log_path,
        "anchor_watermark": producer.env.anchor.watermark_path,
        "c9_path": Path(persisted["c9_db_path"]),
    }
    return persisted, paths


def produce(root, *, gm01=None, case, variant="A_REPAIR_LONG",
            need_e2=True, source=None):
    """Produce the first-class source-bound BP2 artifacts and product inputs."""
    typed = validate_source(source or source_from_case(case), case)
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    producer = _producer(root, typed, variant)
    try:
        if need_e2:
            outcome = producer.run()
            if not outcome.ok:
                raise RuntimeError(
                    "BP2_FIRSTCLASS_REFUSED:"
                    + outcome.stage_reached + ":" + outcome.failure_code)
            receipt = outcome.receipt()
        else:
            partial = producer.run_without_e2()
            flat = producer._flat_receipts(producer.pipeline, None)
            receipt = {
                "schema": "BP2_FIRSTCLASS_RECEIPT@1",
                "ok": True,
                "stage_reached": "c9_commit",
                **flat,
                "no_e2": True,
                "material_access": partial["material_access"],
            }
        persisted, paths = _persisted(producer, receipt)
        artifacts = R._assemble(
            mode="FRESH", root=root / "bp2",
            life=producer.historical_life, persisted=persisted,
            paths=paths, receipt={"persisted": persisted}, e2=None)
        return {
            "producer": producer,
            "artifacts": artifacts,
            "receipt": receipt,
            "source": typed,
            "c8_state_digest": persisted["c8_state_digest"],
            "e1_event_hash": persisted["e1_event_hash"],
            "target_id": persisted["target_id"],
        }
    except Exception:
        producer.close()
        raise


def build_product(root, *, gm01=None, case, variant="A_REPAIR_LONG",
                  need_e2=True, source=None):
    """Build the R31J C12 product over the first-class source artifacts."""
    built = produce(root, gm01=gm01, case=case, variant=variant,
                    need_e2=need_e2, source=source)
    product = R31JProduct(
        Path(root) / "product", artifacts=built["artifacts"],
        source=built["source"], c8_state_digest=built["c8_state_digest"],
        e1_event_hash=built["e1_event_hash"],
        target_id=built["target_id"], variant=variant)
    return product, built, built["producer"]


def c9_only(root, *, gm01=None, case, variant="A_REPAIR_LONG", source=None):
    """Run through C9 with no A E2, preserving lawful NO_CHANGE/refusal."""
    typed = validate_source(source or source_from_case(case), case)
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    producer = _producer(root, typed, variant)
    try:
        return producer.run_without_e2(), producer
    except Exception:
        producer.close()
        raise


__all__ = [
    "MaterialSourceRefusal",
    "PREIMAGE_FIELDS",
    "SHARE_TOOL",
    "build_product",
    "c9_only",
    "case_preimage",
    "material_access",
    "prepare_life",
    "produce",
    "source_from_case",
    "validate_source",
]
