"""R26V sourcefree historically constituted V3 actor/other producer.

Builds two genuinely separate actor ledgers over G18 material histories, a
shared objective encounter, independently performed actions, an independent
other refusal/omission, and explicit unknown relation views. It then consumes
the exact BP2→BP4 chain in this return's staged BP2P4J vendor.

TEST_ONLY. No native ADP007/ADP019/CAN/C8/C11/Pyat authority is issued.
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import bp2p4.bootstrap  # noqa: E402
bp2p4.bootstrap.install()

from bp1.composer import (  # noqa: E402
    TwoActorLife, build_actor_history, issue_default_sources,
)
from bp1.ledger import (  # noqa: E402
    ActorLedger, LedgerRefusal, make_objective_event, verify_snapshot,
)
from bp1.source import issue_actor_source  # noqa: E402
from lab_sgi1.joint import (  # noqa: E402
    material_joint_opportunity, observe_joint_actions, validate_joint,
)

A_ID = "TEST_ONLY_BP1_R26V_ACTOR_A"
B_ID = "TEST_ONLY_BP1_R26V_ACTOR_B"
GRADE = "TEST_ONLY_SOURCEFREE_HISTORICAL_ACTOR_NOT_NATIVE"


@dataclass(frozen=True)
class Genesis:
    variant: str
    a_material: int
    b_material: int
    a_cash: int
    b_cash: int
    a_hours: int
    b_hours: int
    a_birth: int
    b_birth: int
    a_seed: str
    b_seed: str
    joint_time: int
    payment: int
    task_hours: int
    b_refuses_extra: bool = True
    a_declines_optional: bool = True


from dataclasses import replace

VARIANTS = {
    "A_REPAIR_LONG": Genesis(
        "A_REPAIR_LONG", 7, 3, 34, 22, 26, 21, 13, 15,
        "R26V_A_LONG_REPAIR", "R26V_B_SHORT_FINISH", 240, 2, 1),
    "B_RESOURCE_RICH": Genesis(
        "B_RESOURCE_RICH", 4, 6, 20, 41, 18, 31, 16, 12,
        "R26V_A_SHORT_REPAIR", "R26V_B_LONG_FINISH", 260, 3, 2),
}
VARIANTS["B_NO_REFUSAL"] = replace(
    VARIANTS["A_REPAIR_LONG"], variant="B_NO_REFUSAL", b_refuses_extra=False)
VARIANTS["A_NO_OMISSION"] = replace(
    VARIANTS["A_REPAIR_LONG"], variant="A_NO_OMISSION", a_declines_optional=False)
VARIANTS["A_NO_MATERIAL"] = replace(
    VARIANTS["A_REPAIR_LONG"], variant="A_NO_MATERIAL", a_material=0,
    a_cash=0, a_hours=0)


def _sources(g: Genesis):
    a = issue_actor_source(
        actor_id=A_ID, role="repair", seed=g.a_seed, birth_clock=g.a_birth,
        initial_cash=g.a_cash, initial_free_hours=g.a_hours,
        material_units=g.a_material, other_actor_id=B_ID,
        known_unknowns=("CHILDHOOD_HISTORY_SPARSE", "PSYCHOLOGICAL_LAW_UNISSUED",
                        "NATIVE_ACTOR_SOURCE_NOT_GRANTED"))
    b = issue_actor_source(
        actor_id=B_ID, role="finishing", seed=g.b_seed, birth_clock=g.b_birth,
        initial_cash=g.b_cash, initial_free_hours=g.b_hours,
        material_units=g.b_material, other_actor_id=A_ID,
        known_unknowns=("CHILDHOOD_HISTORY_SPARSE", "PSYCHOLOGICAL_LAW_UNISSUED",
                        "NATIVE_ACTOR_SOURCE_NOT_GRANTED"))
    return a, b


def build_life(variant: str = "A_REPAIR_LONG") -> TwoActorLife:
    g = VARIANTS[variant]
    a_source, b_source = _sources(g)
    a_events, a_replay = build_actor_history(a_source)
    b_events, b_replay = build_actor_history(b_source)
    material = material_joint_opportunity(
        effective_index=g.joint_time, units=1, payment_per_actor=g.payment,
        task_hours=g.task_hours)
    anchor = {"actor_id": a_source.actor_id, "history_events": a_events}
    witness = observe_joint_actions(anchor, b_events, material)
    if witness["status"] != "WITNESSED" or not validate_joint(anchor, b_events, witness):
        raise LedgerRefusal("JOINT_PERFORMED_ACTION_NOT_WITNESSED")
    objective = make_objective_event(
        material, witness, [a_source.actor_id, b_source.actor_id])
    a_ledger = ActorLedger(a_source, prior_history_events=a_events)
    b_ledger = ActorLedger(b_source, prior_history_events=b_events)
    for ledger in (a_ledger, b_ledger):
        ledger.append_shared_objective(
            objective, parents=(ledger.prior_history_event_id,))
    a_action = next(x for x in witness["actions"]
                    if x["owner_id"] == a_source.actor_id)
    b_action = next(x for x in witness["actions"]
                    if x["owner_id"] == b_source.actor_id)
    a_ledger.append_performed_action(
        a_action, material, objective["objective_event_id"],
        parents=(a_ledger.prior_history_event_id,
                 a_ledger.objective_events[-1].event_id))
    b_ledger.append_performed_action(
        b_action, material, objective["objective_event_id"],
        parents=(b_ledger.prior_history_event_id,
                 b_ledger.objective_events[-1].event_id))
    a_ledger.append_other_action(
        b_action, material, parents=(a_ledger.objective_events[-1].event_id,))
    b_ledger.append_other_action(
        a_action, material, parents=(b_ledger.objective_events[-1].event_id,))
    a_ledger.append_relation_view(
        b_source.actor_id, "UNKNOWN_OR_NONRECIPROCAL",
        "NO_PSYCHIC_RELATION_OWNER_GRANT",
        parents=(a_ledger.events[-1].event_id,))
    b_ledger.append_relation_view(
        a_source.actor_id, "UNKNOWN_OR_NONRECIPROCAL",
        "NO_PSYCHIC_RELATION_OWNER_GRANT",
        parents=(b_ledger.events[-1].event_id,))
    # B independently refuses an extra voluntary task without A seeing it.
    if g.b_refuses_extra:
        b_ledger.append_no_change(
            "OTHER_REFUSES_VOLUNTARY_EXTRA_TASK",
            parents=(b_ledger.events[-1].event_id,))
    # A independently declines an optional solo task; this is an omission, not
    # a failure to perform the joint obligation.
    if g.a_declines_optional:
        a_ledger.append_no_change(
            "FOCAL_DECLINES_OPTIONAL_TASK",
            parents=(a_ledger.events[-1].event_id,))
    for ledger in (a_ledger, b_ledger):
        ok, errors = ledger.verify()
        if not ok:
            raise LedgerRefusal("HISTORICAL_LEDGER_INVALID:" + ",".join(errors))
    a_snapshot, b_snapshot = a_ledger.snapshot(), b_ledger.snapshot()
    for snap in (a_snapshot, b_snapshot):
        ok, why = verify_snapshot(snap)
        if not ok:
            raise LedgerRefusal("SNAPSHOT_INVALID:" + str(why))
    life = TwoActorLife(
        a_source=a_source, b_source=b_source, a_events=a_events,
        b_events=b_events, a_replay=a_replay, b_replay=b_replay,
        material=material, witness=witness, objective=objective,
        a_ledger=a_ledger, b_ledger=b_ledger,
        a_snapshot=a_snapshot, b_snapshot=b_snapshot)
    # Attach ledger receipts without changing the upstream class.
    life.historical_receipt = {  # type: ignore[attr-defined]
        "schema": "R26V_HISTORICAL_ACTOR_LIFE@1",
        "grade": GRADE,
        "variant": variant,
        "actor_ids": [a_source.actor_id, b_source.actor_id],
        "source_hashes": [a_source.source_hash, b_source.source_hash],
        "snapshot_hashes": [a_snapshot["hash"], b_snapshot["hash"]],
        "event_kinds": {
            a_source.actor_id: [e.kind for e in a_ledger.events],
            b_source.actor_id: [e.kind for e in b_ledger.events],
        },
        "other_refusal": "OTHER_REFUSES_VOLUNTARY_EXTRA_TASK" if g.b_refuses_extra else None,
        "focal_omission": "FOCAL_DECLINES_OPTIONAL_TASK" if g.a_declines_optional else None,
        "native_actor": False, "psychology_claim": False,
    }
    return life


def build_no_development_record(variant: str = "A_REPAIR_LONG") -> dict:
    """H0: sources and sparse genesis, but no performed developmental action."""
    a, b = _sources(VARIANTS[variant])
    return {
        "schema": "R26V_H0_NO_DEVELOPMENT@1",
        "actor_ids": [a.actor_id, b.actor_id],
        "source_hashes": [a.source_hash, b.source_hash],
        "performed_actions": [],
        "practice_established": False,
        "native_actor": False,
        "scientific_status": "H0_NO_DEMONSTRATED_DEVELOPMENT_REMAINS_POSSIBLE",
    }


def _patch_actor_builder():
    import bp2_joined.producer as producer
    import bp2p4.reunion as reunion
    producer.build_two_actor_life = build_life
    reunion.build_two_actor_life = build_life


def run_joined(variant: str = "A_REPAIR_LONG", root=None):
    """Run our historical life through BP2's real C8/C9/E1/E2 and BP4 A0/A2."""
    _patch_actor_builder()
    from bp2_joined.producer import JoinedProducer
    from bp2p4 import reunion as R
    from bp2p4.product import JoinedProduct
    from bp2p4.seed import build_seed
    root = Path(root or (HERE.parent / "evidence" / "runtime" / variant))
    root.mkdir(parents=True, exist_ok=True)
    producer = JoinedProducer(root / "bp2", actor="A")
    try:
        outcome = producer.run()
        if not outcome.ok:
            raise RuntimeError("BP2_PRODUCER_REFUSED:" + outcome.stage_reached + ":" + outcome.failure_code)
        receipt = outcome.receipt()
        persisted = receipt["persisted"]
        life = producer.life
        env = producer.env
        paths = {
            "journal_path": Path(persisted["journal_path"]),
            "key_path": env.key_path, "key_id": env.key_store.key_id,
            "anchor_log": env.anchor.log_path,
            "anchor_watermark": env.anchor.watermark_path,
            "c9_path": Path(persisted["c9_db_path"]),
        }
        artifacts = R._assemble(
            mode="FRESH", root=root / "bp2", life=life,
            persisted=persisted, paths=paths, receipt=receipt, e2=None)
        artifacts.r26v = life.historical_receipt  # type: ignore[attr-defined]
        # Use BP4's real product over a newly assembled BP2 artifact.
        product = JoinedProduct(root / "product", artifacts=artifacts)
        observed = product.observe()
        waited = product.wait(30)
        other = product.other()
        offscreen_kinds = [product.store.world_event(product.branch_id, x)["kind"]
                           for x in waited["offscreen_events"]]
        c12_state = product.store.latest_state(product.branch_id)
        c12_clock = product.store.last_clock(product.branch_id)
        product.close()
        return {
            "schema": "R26V_JOINED_PRODUCT@1",
            "grade": GRADE,
            "variant": variant,
            "life": life.historical_receipt,
            "target_id": artifacts.target_id,
            "target_record_hash": artifacts.target_record_hash,
            "consumed_state_hash": artifacts.consumed_state_hash,
            "c8_state_digest": artifacts.c8_state_digest,
            "e1_event_hash": artifacts.e1_event_hash,
            "rule_a_hash": artifacts.rule_a_hash,
            "rule_t_hash": artifacts.rule_t_hash,
            "response_hash": artifacts.response_hash,
            "grant_hash": artifacts.grant_hash,
            "e2_receipt_hash": artifacts.e2_receipt_hash,
            "a0_claims": [c["kind"] for c in observed["claims"]],
            "a0_projects": observed["self"]["state"]["projects"],
            "a0_tools_remaining": observed["self"]["state"]["tools_remaining"],
            "a2_clock": waited["clock"],
            "a2_offscreen_kinds": offscreen_kinds,
            "a2_other_completed_units": other["public"]["completed_units"],
            "native_claims": observed["native_claims"],
            "c12_world_hash": c12_state["world"]["hash"],
            "c12_clock": c12_clock,
            "artifacts": artifacts,
            "product_root": str(root / "product"),
        }
    finally:
        producer.close()


__all__ = ["VARIANTS", "build_life", "build_no_development_record", "run_joined"]


def r26v_joined_assertion(result: dict, *, expected_target: str | None = None) -> dict:
    """The one named downstream A0/A2 assertion used by every R26V trial."""
    if expected_target is not None and result.get("target_id") != expected_target:
        raise AssertionError("R26V_TARGET_NOT_BOUND_TO_ACTOR_HISTORY")
    if result.get("a0_claims") != ["ARRIVAL"]:
        raise AssertionError("R26V_A0_CLAIMS:" + str(result.get("a0_claims")))
    if result.get("a0_tools_remaining") != 1:
        raise AssertionError("R26V_PRACTICE_TOOL_MISSING")
    if result.get("a2_clock") != 40:
        raise AssertionError("R26V_A2_CLOCK")
    if "OFFSCREEN_REPAIR" not in result.get("a2_offscreen_kinds", []):
        raise AssertionError("R26V_A2_OFFSCREEN_REPAIR_MISSING")
    if result.get("native_claims", {}).get("actor") is not False:
        raise AssertionError("R26V_NATIVE_ACTOR_CLAIM")
    return {
        "assertion": "r26v_joined_assertion",
        "status": "PASS",
        "target_id": result["target_id"],
        "a0_claims": result["a0_claims"],
        "a0_tools_remaining": result["a0_tools_remaining"],
        "a2_clock": result["a2_clock"],
        "a2_offscreen_kinds": result["a2_offscreen_kinds"],
        "a2_other_completed_units": result["a2_other_completed_units"],
        "native": False,
    }
